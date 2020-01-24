import pandas as pd
from datetime import datetime
from datetime import timezone

import os

import matplotlib.pyplot as plt



TRACKS_INPUT_DIR = os.path.join("data", "tracks_TMA_opensky_2018")
STATES_INPUT_DIR = os.path.join("data", "states_TMA_opensky_merged_with_ddr_m3_2018")

TRACKS_TMA_OPENSKY_CSV = "tracks_TMA_opensky_2018_07_week5.csv"
STATES_TMA_OPENSKY_CSV = "states_TMA_opensky_merged_with_ddr_m3_2018_07_week5_fixed.csv"

OUTPUT_DIR = os.path.join("data", "pictures")


ELTOK_lon = 16.6503
ELTOK_lat = 59.5861
HMR_lon = 18.3917
HMR_lat = 60.2794
XILAN_lon = 19.0761
XILAN_lat = 59.6594
NILUG_lon = 17.8847
NILUG_lat = 58.8158

TMA_lon=[18.2130555555556, 18.5547222222222, 18.8469444444444, 19.3136111111111, 19.8280555555556, 19.2736111111111,
          18.9683333333333, 18.7547222222222, 18.5394444444444, 18.4572222222222, 17.9327777777778, 17.4569444444444,
          17.4077777777778, 17.2233333333333, 16.7077777777778, 16.2677777777778, 16.3183333333333, 16.4466666666667,
          17.5966666666667, 18.2130555555556];

TMA_lat=[60.2994444444444, 60.2661111111111, 59.8827777777778, 60.0352777777778, 59.6736111111111, 59.5994444444444,
          59.255, 59.0419444444444, 58.8325, 58.7525, 58.5830555555556, 58.6163888888889, 58.9661111111111,
          58.9786111111111, 59.0119444444444, 59.0494444444444, 59.3238888888889, 59.7494444444444, 60.2327777777778,
          60.2994444444444];

def get_all_states(csv_input_file):
    
    df = pd.read_csv(csv_input_file, sep=' ', index_col=[0,1],
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'velocity', 'endDate', 'aircraftType'],
                    dtype={'flightId':int, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'altitude':int, 'velocity':int, 'endDate':str, 'aircraftType':str})
    
    return df


def get_states_by_time(all_states_df, timestamp_begin, timestamp_end):

    df = all_states_df.copy()
    
    number_of_flights = len(df.groupby(level='flightId'))
    print(len)

    count = 0
    for flight_id, flight_id_group in df.groupby(level='flightId'):
        
        count = count + 1
        #print(number_of_flights, count)

        #end_timestamp = df.loc[flight_id].tail(1)['timestamp'].item()
        end_timestamp = df.loc[flight_id]['timestamp'].values[-1]
        
        if (end_timestamp < timestamp_begin) | (end_timestamp > timestamp_end):
            df = df.drop(flight_id, level='flightId')

    return df


def get_all_tracks(csv_input_file):
    
    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'beginDate', 'callsign', 'icao24', 'endDate', 'time', 'timestamp',
                             'lat', 'lon', 'baroAltitude', 'aircraftType', 'origin'],
                    index_col=[0,1],
                    dtype={'flightId':int, 'sequence':int, 'time':str, 'timestamp':int, 'beginDate':str, 'endDate':str})

    return df


def get_tracks_by_time(all_tracks_df, timestamp_begin, timestamp_end):

    df = all_tracks_df.copy()

    for flight_id, flight_id_group in df.groupby(level='flightId'):
        
        #end_timestamp = df.loc[flight_id].tail(1)['timestamp'].item()
        end_timestamp = df.loc[flight_id]['timestamp'].values[-1]
        
        if (end_timestamp < timestamp_begin) | (end_timestamp > timestamp_end):
            df = df.drop(flight_id, level='flightId')

    return df


def make_traj_lat_opensky_plot(plt, tracks_df, color):

    plt.plot(HMR_lon, HMR_lat, 'ro')
    plt.plot(NILUG_lon, NILUG_lat, 'ro')
    plt.plot(XILAN_lon, XILAN_lat, 'ro')
    plt.plot(ELTOK_lon, ELTOK_lat, 'ro')
    
    count = 0
    for flight_id, new_df in tracks_df.groupby(level='flightId'):
        count = count + 1
        lon = []
        lat = []
        for seq, row in new_df.groupby(level='sequence'):
            lon.append(row.ix[(flight_id, seq)]['lon'])
            lat.append(row.ix[(flight_id, seq)]['lat'])
        
        plt.plot(lon, lat, color=color, linewidth=3)
        
    print("***********************")
    print(count)
        
        
def save_traj_lat_plots(full_filename_lat, TMA_tracks_opensky_df):
    
    plt.figure(figsize=(9,6))
    
    make_traj_lat_opensky_plot(plt, TMA_tracks_opensky_df, "orange")
    
    min_lon = min(TMA_lon)
    min_lat = min(TMA_lat)
    max_lon = max(TMA_lon)
    max_lat = max(TMA_lat)
    
    plt.axis('equal')
    plt.axis([min_lon, max_lon, min_lat, max_lat])
    
    #plt.show()
    plt.savefig(full_filename_lat)
    
    plt.gcf().clear()         

'''
DATE_TIME_BEGIN = datetime(2018, 7, 29, 5, 0, 0, 0, timezone.utc)
DATE_TIME_END = datetime(2018, 7, 29, 12, 0, 0, 0, timezone.utc)
timestamp_begin =  datetime.timestamp(DATE_TIME_BEGIN)
timestamp_end =  datetime.timestamp(DATE_TIME_END)

TMA_all_tracks_opensky_df = get_all_tracks(os.path.join(TRACKS_INPUT_DIR, TRACKS_TMA_OPENSKY_CSV))
TMA_all_tracks_opensky_df = get_tracks_by_time(TMA_all_tracks_opensky_df, timestamp_begin, timestamp_end)
TMA_all_tracks_opensky_df.reset_index(drop=False, inplace=True)
TMA_all_tracks_opensky_df.to_csv(os.path.join(TRACKS_INPUT_DIR, "tracks_TMA_opensky_2018_07_29.csv"),
                                 sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=False)

'''


TMA_all_tracks_opensky_df = get_all_tracks(os.path.join(TRACKS_INPUT_DIR, "tracks_TMA_opensky_2018_07_29.csv"))



for hour in range(5, 12): # (5, 12)
    TRACKS_TMA_OPENSKY_PNG = "tracks_TMA_openksy_180729_" + str(hour) +".png"

    DATE_TIME_BEGIN = datetime(2018, 7, 29, hour, 0, 0, 0, timezone.utc)
    DATE_TIME_END = datetime(2018, 7, 29, hour+1, 0, 0, 0, timezone.utc)

    timestamp_begin =  datetime.timestamp(DATE_TIME_BEGIN)
    timestamp_end =  datetime.timestamp(DATE_TIME_END)



    TMA_tracks_opensky_df = get_tracks_by_time(TMA_all_tracks_opensky_df, timestamp_begin, timestamp_end)
    TMA_tracks_opensky_df.to_csv(os.path.join(OUTPUT_DIR, "temp.csv"),
                                 sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=True)

    count = 0
    
    #print("Tracks")
    #for flight_id, flight_id_group in TMA_tracks_opensky_df.groupby(level='flightId'):        
    #    count = count + 1
    #    print(flight_id)
        
    #print(count)

    save_traj_lat_plots(os.path.join(OUTPUT_DIR, TRACKS_TMA_OPENSKY_PNG), TMA_tracks_opensky_df)
