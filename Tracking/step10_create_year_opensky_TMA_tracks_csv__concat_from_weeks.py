import pandas as pd
import os

from datetime import datetime
import calendar

import time
start_time = time.time()

year = '2018'
DATA_DIR = os.path.join("data", "tracks_TMA_opensky_" + year)

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#months = ['01']

opensky_df = pd.DataFrame(columns=['flightId', 'sequence', 'endDate', 'callsign',
                  'icao24', 'date', 'time', 'timestamp', 'lat', 'lon', 'baroAltitude', 'aircraftType', 'origin'])

for month in months:
    print(month)
    
    number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
    for week in range(0, number_of_weeks):

        filename = 'tracks_TMA_opensky_' + year + '_' + month + '_week' + str(week + 1) + '.csv'

        df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names = ['flightId', 'sequence', 'endDate', 'callsign',
                  'icao24', 'date', 'time', 'timestamp', 'lat', 'lon', 'baroAltitude', 'aircraftType', 'origin'], dtype = {'date': str})
        opensky_df = opensky_df.append(df, ignore_index=True)


filename = "tracks_TMA_opensky_" + year + ".csv"

opensky_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.6f', index=False, header=None)

print((time.time()-start_time)/60)

