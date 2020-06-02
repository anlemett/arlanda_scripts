import pandas as pd
import numpy as np

from constants import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


import os

year = "2018"

DATA_DIR = "data"


def get_all_tracks(month, is_m1):
    
    if is_m1:
        INPUT_DIR = os.path.join(DATA_DIR, "tracks_ddr_m1_" + year)
        filename = os.path.join(INPUT_DIR, 'tracks_ddr_m1_' + year + '_' + month + '.csv')
    else:
        INPUT_DIR = os.path.join(DATA_DIR, "tracks_ddr_m3_" + year)
        filename = os.path.join(INPUT_DIR, 'tracks_ddr_m3_' + year + '_' + month + '.csv')


    df = pd.read_csv(filename, sep=' ',
                    names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                           'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                           'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                     index_col=[0,1],
                     dtype={'flightId':int, 'sequence':int, 'beginTime':str, 'endTime':str, 'beginDate':str, 'endDate':str})
    
    enroute_flight_num = len(df.groupby(level='flightId'))
    print("Enroute flight number: ", enroute_flight_num)
    
    return df


def get_tracks_inside_TMA(month, tracks_df, is_m1):
    
    if is_m1:
        OUTPUT_DIR = os.path.join(DATA_DIR, "tracks_TMA_ddr_m1_" + year)
        filename = os.path.join(OUTPUT_DIR, 'tracks_TMA_ddr_m1_' + year + '_' + month + '.csv')
    else:
        OUTPUT_DIR = os.path.join(DATA_DIR, "tracks_TMA_ddr_m3_" + year)
        filename = os.path.join(OUTPUT_DIR, 'tracks_TMA_ddr_m3_' + year + '_' + month + '.csv')


    tracks_inside_TMA_df = pd.DataFrame()

    number_of_flights = len(tracks_df.groupby(level='flightId'))
    count = 1
    for flight_id, flight_id_group in tracks_df.groupby(level='flightId'):
        print(month, number_of_flights, count)
        count = count + 1
        entry_point_index = get_entry_point_index(flight_id, flight_id_group)
        flight_id_group_inside_TMA = flight_id_group.iloc[entry_point_index-1:]
        
        #if flight_id_group.iloc[entry_point_index-1]['endDate'] == flight_id_group.iloc[-1]['endDate']:
        tracks_inside_TMA_df = tracks_inside_TMA_df.append(flight_id_group_inside_TMA)
            
    #print(tracks_inside_TMA_df)
        
    TMA_flight_num = len(tracks_inside_TMA_df.groupby(level='flightId'))
    print("TMA flight number: ", TMA_flight_num)
    tracks_inside_TMA_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.6f', header=None)


def get_entry_point_index(flight_id, flight_id_group):
    for seq, row in flight_id_group.groupby(level='sequence'):
        
        segmentId = row.loc[(flight_id, seq)]['segmentId']

        if segmentId.startswith('HMR') or segmentId.startswith('NILUG') or segmentId.startswith('XILAN') or segmentId.startswith('ELTOK'):
            return seq

    for seq, row in flight_id_group.groupby(level='sequence'):
        if (check_TMA_contains_point(Point(row.loc[(flight_id, seq)]['beginLon'], row.loc[(flight_id, seq)]['beginLat']))):
            return seq

    return 0


def check_TMA_contains_point(point):

    lons_lats_vect = np.column_stack((TMA_lon, TMA_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)  # check if polygon contains point


import time
time_start = time.time()

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:
    
    all_tracks_m1_df = get_all_tracks(month, True)
    get_tracks_inside_TMA(month, all_tracks_m1_df, True)
    
    print("m1", month)

print((time.time()-time_start)/60)


for month in months:
    
    all_tracks_m3_df = get_all_tracks(month, False)
    get_tracks_inside_TMA(month, all_tracks_m3_df, False)
    
    print("m3", month)

print((time.time()-time_start)/60)
