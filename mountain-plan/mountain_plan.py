import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

class mountain_gather(object):
    def __init__(self):
        self.BASE_URL = """https://www.mountain-forecast.com"""
        
        self.value_pulls = {'rain':['forecast__table-rain','forecast__table-value'],                    # Unit: cm
                            'snow':['forecast__table-snow','forecast__table-value'],                    # Unit: cm
                            'temp_max':['forecast__table-max-temperature','forecast__table-value'],     # Unit: C
                            'temp_min':['forecast__table-min-temperature','forecast__table-value'],     # Unit: C
                            'chill':['forecast__table-chill','forecast__table-value'],                  # Unit: C
                            'freeze_level':['forecast__table-freezing-level','heightfl']}               # Unit: m
        self.payload = {}
    
    def _get_forecast_url(self, mountain_name):
        r = requests.get(f"{self.BASE_URL}/peaks/{mountain_name}")
        soup = BeautifulSoup(r.text, 'html.parser')
        forecast_tag = soup.find(name='li',attrs={'class':'tabs__list-item'}).find(name='a')
        forecast_link = forecast_tag.attrs['href']
        return forecast_link

    def _generic_data_retrieval(self, forecast_table, value_id, span_id):
        overall = forecast_table.find(name='tr', attrs={'class':value_id})
        tags = overall.find_all(name="span", attrs={'class':span_id})
        vals = [int(i.text.strip('\n -').replace('','0')) for i in tags]
        return vals

    @staticmethod
    def _expand_days(days, day_periods):
        expanded_days = []
        if day_periods[0] == 'AM':
            primary_day_count = 3
        elif day_periods[0] == 'PM':
            primary_day_count = 2
        else:
            primary_day_count = 1
        ### Check day
        if int(days[0].split('_')[-1]) == datetime.datetime.now().day:
            today = datetime.datetime.today().date()
        elif int(days[0].split('_')[-1]) == datetime.datetime.now().day-1:
            today = (datetime.datetime.today() - datetime.timedelta(days=1)).date()
        elif int(days[0].split('_')[-1]) == datetime.datetime.now().day+1:
            today = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
        else:
            assert "WTF Time is BROKEN"
        
        for a in range(primary_day_count):
            expanded_days.append(today)
        current_day = today + datetime.timedelta(days=1)
        while len(expanded_days) < len(day_periods):
            for day in days[1:]:
                [expanded_days.append(current_day) for a in range(3)]
                current_day = current_day + datetime.timedelta(days=1)
        return expanded_days[:len(day_periods)]
    
    def _get_day_periods(self, ret=False):
        day_tags = self.forecast_table.find_all(name='td' , attrs={'class':'forecast__table-days-item'})
        days = [day.attrs['data-column-name'] for day in day_tags]
        
        
        day_period_tags = self.forecast_table.find_all(name="td", attrs={'class':'forecast__table-time-item'})
        day_periods = [i.find('span').text.strip('\n ') for i in day_period_tags]
        self.payload['day_periods'] = day_periods
        
        expanded_days = self._expand_days(days, day_periods)
        self.payload['days'] = expanded_days
        
        if ret:
            return (expanded_days, day_periods)
        
    def _get_weather_summary(self, ret=False):
        weather_tags = self.forecast_table.find(name='tr',
                                                attrs='forecast__table-weather'
                                               ).find_all(name='div',
                                                          attrs={'class':'icon-weather'})
        period_weather = [i.find('img').attrs['alt'] for i in weather_tags]
        self.payload['period_weather'] = period_weather

        wind_overall = self.forecast_table.find(name='tr', attrs={'class':'forecast__table-wind'})
        wind_tags = wind_overall.find_all(name="div", attrs={'class':'windcell'})
        period_wind = [i.find('img').attrs['alt'] for i in wind_tags]
        
        self.payload['period_wind'] = period_wind
        if ret:
            return (period_weather, period_wind)
        
    def _cleanup(self):
        self.mountain_frame[['wind_value','wind_direction']] = self.mountain_frame.period_wind.apply( 
                                                lambda x: pd.Series(str(x).split(" ")))
        self.mountain_frame['wind_value'] = self.mountain_frame['wind_value'].astype(int)
#         self.mountain_frame[['dow','day']] = self.mountain_frame.days.apply( 
#                                                 lambda x: pd.Series(str(x).split("_")))
        
        
    def get_measures(self):
        for measure, ids in self.value_pulls.items():
            metric = self.value_pulls[measure]
            self.payload[measure] = self._generic_data_retrieval(forecast_table=self.forecast_table,
                                                                 value_id=ids[0],
                                                                 span_id=ids[1])

    def run(self, mountain_name):
        self.payload = {}                                                    # Reset paload for this run
        forecast_url = self._get_forecast_url(mountain_name=mountain_name)   # Fetch full URL
        r = requests.get(f"{self.BASE_URL}/{forecast_url}")                  # Fetch full page
        self.page_soup = BeautifulSoup(r.text, 'html.parser')
        self.forecast_table = self.page_soup.find(name='table', attrs={'class':'forecast__table'})
        self._get_day_periods()
        self._get_weather_summary()
        self.get_measures()
        self.mountain_frame = pd.DataFrame(self.payload)
        self._cleanup()
        print(f'Retrieval for {mountain_name} Complete')
        return 0