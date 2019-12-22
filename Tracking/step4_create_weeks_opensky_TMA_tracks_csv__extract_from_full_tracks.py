import pandas as pd
import numpy as np
import calendar

from constants import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import os

year = '2018'

DATA_INPUT_DIR = os.path.join("data", "tracks_opensky_merged_with_ddr_m3_" + year)

DATA_OUTPUT_DIR = os.path.join("data", "tracks_TMA_opensky_" + year)


def get_all_tracks(csv_input_file):

    df = pd.read_csv(os.path.join(DATA_INPUT_DIR, csv_input_file), sep=' ',
                    names = ['flightId', 'sequence', 'beginDate', 'callsign', 'icao24', 'date', 'time', 'timestamp',
                             'lat', 'lon', 'baroAltitude', 'aircraftType', 'origin'],
                    index_col=[0,1],
                    dtype={'flightId':int, 'sequence':int, 'time':str, 'beginDate':str, 'date':str})
    return df


def get_tracks_inside_TMA(month, week, tracks_df, csv_output_file):

    tracks_inside_TMA_df = pd.DataFrame()

    number_of_flights = len(tracks_df.groupby(level='flightId'))
    count = 1
    for flight_id, new_df in tracks_df.groupby(level='flightId'):
        print(month, week, number_of_flights, count)
        count = count + 1
        entry_point_index = get_entry_point_index(flight_id, new_df)
        new_df_inside_TMA = new_df.iloc[entry_point_index-1:]
        #if new_df.iloc[entry_point_index-1]['date'] == new_df.iloc[-1]['date']:
        tracks_inside_TMA_df = tracks_inside_TMA_df.append(new_df_inside_TMA)

    tracks_inside_TMA_df.to_csv(os.path.join(DATA_OUTPUT_DIR, csv_output_file), sep=' ', encoding='utf-8', float_format='%.6f', header=None)


def get_entry_point_index(flight_id, new_df):
    for seq, row in new_df.groupby(level='sequence'):
        if (check_TMA_contains_point(Point(row.ix[(flight_id, seq)]['lon'], row.ix[(flight_id, seq)]['lat']))):
            return seq
    return 0


def check_TMA_contains_point(point):

    lons_lats_vect = np.column_stack((TMA_lon, TMA_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)  


def extract_TMA_part(month, week):
    
    input_filename = 'tracks_opensky_merged_with_ddr_m3_' + year + '_' + month + '_week' + str(week) + '.csv' 

    all_tracks_df = get_all_tracks(input_filename)
        
    output_filename = 'tracks_TMA_opensky_' + year + '_' + month + '_week' + str(week) + '.csv' 
        
    get_tracks_inside_TMA(month, week, all_tracks_df, output_filename)
    

import time
start_time = time.time()

from multiprocessing import Process

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:

    #number_of_weeks = 5
    #if month == '02' and not calendar.isleap(int(year)):
    #    number_of_weeks = 4
        
    procs = [] 
    
    number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
#    for week in range(0, number_of_weeks):
    for week in range(1, 2):
        
        proc = Process(target=extract_TMA_part, args=(month, week + 1,))
        procs.append(proc)
        proc.start()
        
        
    # complete the processes      
    for proc in procs:
        proc.join()
            
print((time.time()-start_time)/60)
