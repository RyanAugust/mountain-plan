from datetime import datetime, timedelta
print('Beginning Test\n-----------------')
print('Attempting to import module...')
import trip_planner
print('---passed---')

#### Segment Class
print('Attempting to set segment details...')
first = trip_planner.segment(segment_name='first',segment_start=datetime.now(), segment_time=timedelta(hours=2))
print('---passed---')

print('Attempting to solve segment...')
first.solver()
print('---passed---')

print('Attempting to show segment details...')
print(first)
print('---passed---')

#### Trip Timer Class
print('Attempting to establish trip (4 segments)...')
baldy = trip_planner.trip('Baldy')
baldy.add_segment(segment_name='drive to baldy', 
				  segment_time=timedelta(hours=1, minutes=30))
baldy.add_segment(segment_name='baldy ascent', 
				  segment_time=timedelta(hours=2, minutes=40),
				  segment_end=datetime(year=2020, month=11, day=26, hour=7, minute=1))
baldy.add_segment(segment_name='baldy descent', 
				  segment_time=timedelta(hours=1, minutes=50))
baldy.add_segment(segment_name='drive back from baldy', 
				  segment_time=timedelta(hours=1, minutes=30))
print('---passed---')

print('Attempting to solve...')
baldy.solver(max_depth=5)
print('---passed---')

print('Attempting to show segment details...')
baldy.show_segments()
print('---passed---')
