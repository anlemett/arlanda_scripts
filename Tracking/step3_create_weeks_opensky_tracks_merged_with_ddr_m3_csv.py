from datetime import datetime

import os

year = '2018'

import time
start_time = time.time()

DDR_INPUT_DIR = os.path.join("data", "tracks_ddr_m3_" + year)
ddr_m3_filename = os.path.join(DDR_INPUT_DIR, 'tracks_ddr_m3_' + year + '.csv')

OPENSKY_INPUT_DIR = os.path.join("data", "tracks_opensky_downloaded_" + year)

OUTPUT_DIR = os.path.join("data", "tracks_opensky_merged_with_ddr_m3_" + year)

import pandas as pd
import calendar


def create_merged_week_csv(month, week):
    
    filename = 'tracks_opensky_downloaded_' + year + '_' + month + '_week' + str(week) + '.csv'
    opensky_df = pd.read_csv(os.path.join(OPENSKY_INPUT_DIR, filename), sep=' ',
                    names=['sequence', 'origin', 'endDate', 'callsign', 'icao24', 'date', 'time', 'timestamp',
                    'lat', 'lon', 'baroAltitude'],
                    dtype=str
                    )
    opensky_df.reset_index(drop=True, inplace=True)

    opensky_df.drop(['origin'], axis=1, inplace=True)
    new_opensky_df = pd.merge(opensky_df, ddr_flightId_df, on=['callsign', 'endDate'], how='inner')
    opensky_df = pd.DataFrame()

    new_opensky_df.dropna(inplace=True, how='any', axis=0)
    new_opensky_df = new_opensky_df.astype({"flightId": int})

    new_opensky_df.drop_duplicates(subset=['flightId', 'sequence'], inplace=True)

    new_opensky_df.set_index(['flightId', 'sequence'], inplace=True)
        
        
    filename = 'tracks_opensky_merged_with_ddr_m3_' + year + '_' +month + '_week' + str(week) + '.csv' 

    new_opensky_df.to_csv(os.path.join(OUTPUT_DIR, filename), sep=' ', encoding='utf-8', header=None)

    print(month, week, len(new_opensky_df.groupby(level='flightId')))
    

ddr_df = pd.read_csv(ddr_m3_filename, sep=' ',
                        names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                        'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                        'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                        index_col=[0,1],
                        dtype=str
                        )

ddr_flight_end_df = pd.DataFrame()
print("ddr_flight_end_df")
for flight_id, flight_id_group in ddr_df.groupby(level='flightId'):
     ddr_flight_end_df = ddr_flight_end_df.append(flight_id_group.tail(1))
    
ddr_flight_end_df.reset_index(drop=False, inplace=True)

print(ddr_flight_end_df.head())

ddr_df = pd.DataFrame()

print("ddr_flightId_df")
#'origin' field values are provided by Opensky API but not for all aircraft, so we substitute them by ddr data
ddr_flightId_df = ddr_flight_end_df[['callsign', 'endDate', 'flightId', 'aircraftType', 'origin']].copy()
ddr_flightId_df.to_csv(os.path.join(OUTPUT_DIR, "ddr_flightId.csv"), sep=' ', encoding='utf-8', header=True)


from multiprocessing import Process

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:
    print("month", month)

    #number_of_weeks = 5
    #if month == '02' and not calendar.isleap(int(year)):
    #    number_of_weeks = 4
    
    procs = [] 
        
    number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
    for week in range(0, number_of_weeks):
        
        proc = Process(target=create_merged_week_csv, args=(month, week + 1,))
        procs.append(proc)
        proc.start()
        #create_merged_week_csv(month, week + 1)
        
    # complete the processes      
    for proc in procs:
        proc.join()

print((time.time()-start_time)/60)

