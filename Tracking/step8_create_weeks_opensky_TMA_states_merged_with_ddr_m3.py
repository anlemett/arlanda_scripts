import os

year = "2018"

DDR_INPUT_DIR = os.path.join("data", "tracks_ddr_m3_" + year)

OPENSKY_INPUT_DIR = os.path.join("data", "states_TMA_opensky_downloaded_" + year)

OUTPUT_DIR = os.path.join("data", "states_TMA_opensky_merged_with_ddr_m3_" + year)

import pandas as pd
import calendar

import time
start_time = time.time()

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:
    
    ddr_m3_filename = os.path.join(DDR_INPUT_DIR, 'tracks_ddr_m3_' + year + '_' + month + '.csv')

    ddr_df = pd.read_csv(ddr_m3_filename, sep=' ',
                        names=['flight_id', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                        'beginFL', 'endFL', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                        'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                        dtype=str
                        )

    ddr_flight_begin_df = ddr_df[ddr_df['sequence'] == "1"]
    ddr_flight_begin_df.reset_index(drop=True, inplace=True)
    ddr_df = pd.DataFrame()

    ddr_flightId_df = ddr_flight_begin_df[['flight_id', 'aircraftType']].copy()
    

    number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
    for week in range(0, number_of_weeks):
    
        opensky_states_filename = 'states_TMA_opensky_downloaded_' + year + '_' + month + '_week' + str(week + 1) + '.csv'
        opensky_states_merged_with_ddr_m3_filename = 'states_TMA_opensky_merged_with_ddr_m3_' + year + '_' + month + '_' + str(week + 1) + '.csv'

    
        opensky_df = pd.read_csv(os.path.join(OPENSKY_INPUT_DIR, opensky_states_filename), sep=' ',
                    names=['flight_id', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'velocity', 'beginDate'],
                    dtype=str
                    #dtype={'flight_id':str, 'timestamp':int}
                    )
        opensky_df.reset_index(drop=True, inplace=True)


        new_opensky_df = pd.merge(opensky_df, ddr_flightId_df, on=['flight_id'], how='left')
        opensky_df = pd.DataFrame()

        new_opensky_df.dropna(inplace=True, how='any', axis=0)
        new_opensky_df = new_opensky_df.astype({"flight_id": int})

        new_opensky_df.drop_duplicates(subset=['flight_id', 'sequence'], inplace=True)

        new_opensky_df.set_index(['flight_id', 'sequence'], inplace=True)

        #print(new_opensky_df.head())

        new_opensky_df.to_csv(os.path.join(OUTPUT_DIR, opensky_states_merged_with_ddr_m3_filename), sep=' ', encoding='utf-8', header=None)

print((time.time()-start_time)/60)
