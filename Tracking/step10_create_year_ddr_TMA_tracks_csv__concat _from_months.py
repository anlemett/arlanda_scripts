import pandas as pd
import os

import time
start_time = time.time()

year = "2018"

DATA_DIR = os.path.join("data", "tracks_TMA_ddr_m1_" + year)

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

frames = []

for month in months:
    filename = os.path.join(DATA_DIR, "tracks_TMA_ddr_m1_" + year + "_" + month + ".csv")
    df = pd.read_csv(filename, sep=' ', 
                  names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                         'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                         'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                  #index_col=[0,1],
                  dtype = str)
    
    frames.append(df)

tracks_TMA_ddr_m1_df = pd.concat(frames)

filename = os.path.join(DATA_DIR, "tracks_TMA_ddr_m1_" + year + ".csv")
tracks_TMA_ddr_m1_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.6f', index=False, header=None)

tracks_TMA_ddr_m1_df = pd.DataFrame()


DATA_DIR = os.path.join("data", "tracks_TMA_ddr_m3_" + year)

frames = []

for month in months:
    filename = os.path.join(DATA_DIR, "tracks_TMA_ddr_m3_" + year + "_" + month + ".csv")
    df = pd.read_csv(filename, sep=' ', 
                  names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                         'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                         'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                  #index_col=[0,1],
                  dtype = str)

    frames.append(df)

tracks_TMA_ddr_m3_df = pd.concat(frames)

filename = os.path.join(DATA_DIR, "tracks_TMA_ddr_m3_" + year + ".csv")
tracks_TMA_ddr_m3_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.6f', index=False, header=None)

print((time.time()-start_time)/60)
