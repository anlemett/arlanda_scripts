from datetime import datetime
from datetime import timezone

import os

year = '2020'

import time
start_time = time.time()


OPENSKY_INPUT_DIR = os.path.join("data", "tracks_opensky_downloaded_" + year)


import pandas as pd
import calendar


def find_hour_with_max_number_of_flights(month, week):
    
    filename = 'tracks_opensky_downloaded_' + year + '_' + month + '_week' + str(week) + '.csv'
    opensky_df = pd.read_csv(os.path.join(OPENSKY_INPUT_DIR, filename), sep=' ',
                    names=['sequence', 'origin', 'endDate', 'callsign', 'icao24', 'date', 'time', 'timestamp',
                    'lat', 'lon', 'baroAltitude'],
                    dtype=str
                    )
    opensky_df.reset_index(drop=True, inplace=True)

    opensky_df.drop(['sequence', 'origin', 'icao24', 'date', 'time', 'lat', 'lon', 'baroAltitude'], axis=1, inplace=True)
    # now we have: 'endDate', 'callsign', 'timestamp'
    
    opensky_df.set_index(['endDate'], inplace=True)
    
    
    
    
# create flight df

    flight_df = pd.DataFrame(columns=['end_date', 'hour', 'callsign'])
    
    
    
    for date, date_df in opensky_df.groupby(level='endDate'):
        
        date_df = date_df.drop_duplicates(subset='callsign', keep="last")
        
        date_df.set_index(['callsign'], inplace=True)
        
        for callsign, callsign_df in date_df.groupby(level='callsign'):
            
            callsign_df = callsign_df.astype({"timestamp": int})
    
            end_timestamp = callsign_df.loc[callsign]['timestamp']
            end_datetime = datetime.utcfromtimestamp(end_timestamp)
            end_hour_str = end_datetime.strftime('%H')
    
    
            flight_df = flight_df.append({'end_date': date, 'hour': end_hour_str, 'callsign': callsign}, ignore_index=True)
    
   
    number_of_flights_df = pd.DataFrame(columns=['date', 'hour', 'number_of_flights']) 
    
    
    flight_df.set_index(['end_date'], inplace=True)
    
    for date, date_df in flight_df.groupby(level='end_date'):
        
        date_df.set_index(['hour'], inplace=True)
        
        for hour, hour_df in date_df.groupby(level='hour'):
            
            number_of_flights = len(hour_df)
            
            number_of_flights_df = number_of_flights_df.append({'date': date, 'hour': hour, 'number_of_flights': number_of_flights}, ignore_index=True)
        
    number_of_flights_df = number_of_flights_df[number_of_flights_df['number_of_flights']==number_of_flights_df['number_of_flights'].max()]
   
    print(number_of_flights_df)



#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
months = ['04']


max_flight_date = 0
max_flight_hour = 0
max_flight_number = 0
'''
for month in months:
    print("month", month)

    number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
    for week in range(1, number_of_weeks+1):

        find_hour_with_max_number_of_flights(month, week)
'''

month = '04'
week = 1
day = '03'
endDate = '20' + month + day

filename = 'tracks_opensky_downloaded_' + year + '_' + month + '_week' + str(week) + '.csv'
opensky_df = pd.read_csv(os.path.join(OPENSKY_INPUT_DIR, filename), sep=' ',
                    names=['sequence', 'origin', 'endDate', 'callsign', 'icao24', 'date', 'time', 'timestamp',
                    'lat', 'lon', 'baroAltitude'],
                    dtype={'endDate':str, 'timestamp':int}
                    )
opensky_df.reset_index(drop=True, inplace=True)

opensky_df.drop(['sequence', 'origin', 'date', 'time', 'lat', 'lon', 'baroAltitude'], axis=1, inplace=True)

opensky_df = opensky_df[opensky_df['endDate']==endDate]
# now we have: 'endDate', 'callsign', 'timestamp', 'icao24', 
    

hour_begin = datetime(int(year), int(month), int(day) , 14, 0, 0, 0, timezone.utc)
hour_end = datetime(int(year), int(month), int(day) , 15, 0, 0, 0, timezone.utc)

hour_begin_timestamp = hour_begin.timestamp()
hour_end_timestamp = hour_end.timestamp()

opensky_df = opensky_df.drop_duplicates(subset='callsign', keep="last")
opensky_df = opensky_df[(opensky_df['timestamp']>=hour_begin_timestamp)&(opensky_df['timestamp']<hour_end_timestamp)]

   
print(opensky_df)    

print((time.time()-start_time)/60)

