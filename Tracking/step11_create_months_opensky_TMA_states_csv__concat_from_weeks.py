import pandas as pd
import os
import calendar

import time
start_time = time.time()

year = '2018'
DATA_DIR = os.path.join("data", "states_TMA_opensky_merged_with_ddr_m3_" + year)

months = ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:
    print(month)
    
    opensky_states_df = pd.DataFrame(columns=['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'velocity', 'endDate', 'aircraftType'])
    
    number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
    for week in range(0, number_of_weeks):

        filename = 'states_TMA_opensky_merged_with_ddr_m3_' + year + '_' + month + '_week' + str(week + 1) + '.csv'
    
        df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'velocity', 'endDate', 'aircraftType'],
                     dtype = {'date': str})
        
        opensky_states_df = opensky_states_df.append(df, ignore_index=True)

    filename = 'states_TMA_opensky_' + year + '_' + month + '.csv'
    opensky_states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.6f', index=False, header=None)

print((time.time()-start_time)/60)
