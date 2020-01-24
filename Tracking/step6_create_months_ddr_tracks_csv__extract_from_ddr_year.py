from datetime import datetime
from datetime import timezone

import pandas as pd

import os

year = "2018"

M1_DATA_DIR = os.path.join("data", "tracks_ddr_m1_" + year)
M3_DATA_DIR = os.path.join("data", "tracks_ddr_m3_" + year)


def get_ddr_month(date_time_begin, date_time_end, is_m1):
    
    year_month = date_time_begin.strftime("_%Y_%m")
    
    ddr_filename = os.path.join(M3_DATA_DIR, "tracks_ddr_m3_" + year + ".csv")
    ddr_month_filename = os.path.join(M3_DATA_DIR, 'tracks_ddr_m3' + year_month + '.csv')

    
    if is_m1:
        
        ddr_filename = os.path.join(M1_DATA_DIR, "tracks_ddr_m1_" + year + ".csv")
        ddr_month_filename = os.path.join(M1_DATA_DIR, 'tracks_ddr_m1' + year_month + '.csv')

    ddr_df = pd.read_csv(ddr_filename, sep=' ', header=None,
        names=['flightId', 'sequence', 'segmentId', 'origin', 'destination',
               'aircraftType', 'beginTime', 'endTime', 'beginAltitude',
               'endAltitude', 'status', 'callsign', 'beginDate', 'endDate',
               'beginLat', 'beginLon', 'endLat', 'endLon', 'segmentLength',
               'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
        index_col=[0,1],
        dtype=str)

    begin_date = date_time_begin.strftime("%y%m%d")
    end_date = date_time_end.strftime("%y%m%d")

    month_flight_ids = []
    
    for flight_id, new_df in ddr_df.groupby(level='flightId'):
        
       flight_end_date = new_df.iloc[-1]['endDate']
       
       if ((flight_end_date>= begin_date) & (flight_end_date<end_date)):
           month_flight_ids.append(flight_id)


    print(len(month_flight_ids))
    
    ddr_month_df = pd.DataFrame(columns = ['flightId', 'sequence', 'segmentId', 'origin', 'destination',
               'aircraftType', 'beginTime', 'endTime', 'beginAltitude',
               'endAltitude', 'status', 'callsign', 'beginDate', 'endDate',
               'beginLat', 'beginLon', 'endLat', 'endLon', 'segmentLength',
               'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
               index=[0,1],
               dtype=str)
    
    frames = []
    for flight_id, new_df in ddr_df.groupby(level='flightId'):
        if flight_id in month_flight_ids:
            frames.append(new_df)

    ddr_month_df = pd.concat(frames)
    
  
    ddr_month_df.reset_index(inplace=True)
    ddr_month_df.to_csv(ddr_month_filename, sep=' ', encoding='utf-8', header=None, index=False)
    #print(ddr_month_df.head())
    print(ddr_month_filename)

    ddr_df = pd.DataFrame()
    ddr_month_df = pd.DataFrame()

    print(is_m1, year_month)

    

import time
start_time = time.time()

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:
    #UTC time:
    DATE_TIME_BEGIN = datetime(int(year), int(month), 1, 0, 0, 0, 0, timezone.utc)
    if month == '12':
        DATE_TIME_END = datetime(int(year) + 1, 1, 1, 0, 0, 0, 0, timezone.utc)
    else:
        DATE_TIME_END = datetime(int(year), int(month) + 1, 1, 0, 0, 0, 0, timezone.utc)

    #get_ddr_month(DATE_TIME_BEGIN, DATE_TIME_END, True)
    get_ddr_month(DATE_TIME_BEGIN, DATE_TIME_END, False)

print((time.time()-start_time)/60)

