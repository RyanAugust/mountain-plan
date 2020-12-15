import mountain_plan
import pandas as pd

mg = mountain_plan.mountain_gather()
mountain_list = ['Mount-Sill','Mount-Wilson-California','Mount-Whitney',
                 'Mount-Williamson','Split-Mountain','Mount-Ritter',
                 'Mount-Conness','Mount-Baldy-San-Gabriel','Split-Mountain',
                 'Minarets-California','Half-Dome']
current_run = pd.DataFrame()

for mountain_name in mountain_list:
        mg.run(mountain_name)
        frame = mg.mountain_frame
        frame['mountain_name'] = mountain_name
        current_run = current_run.append(frame)
