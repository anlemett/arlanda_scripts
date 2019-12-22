import pandas as pd
from constants import *

csv_input_file = "opensky_tracks_SAS410_1_01_2018.csv"
df_opensky_tracks = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'beginDate', 'callsign', 'icao24', 'date', 'time', 'timestamp',
                    'lat', 'lon', 'baroAltitude', 'aircraftType', 'origin'],
                    index_col=[0,1],
                    dtype={'flightId':int, 'sequence':int, 'timestamp':int, 'beginDate': str, 'time': str, 'date':str})

csv_input_file = "opensky_states_SAS410_1_01.csv"
df_opensky_states = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'callsign', 'lat', 'lon', 'altitude', 'velocity', 'date'],
                    index_col=[0,1],
                    dtype={'flightId':int, 'sequence':int, 'timestamp':int, 'date':str})


import matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(9,6))
plt.xlabel('Timestamp [sec]', fontsize=25)
plt.ylabel('Altitude [m]', fontsize=25)

for flight_id, flight_id_group in df_opensky_states.groupby(level='flightId'):

    opensky_states_timestamps = []
    opensky_states_altitudes = []
    
    for seq, row in flight_id_group.groupby(level='sequence'):
        opensky_states_timestamps.append(row['timestamp'].item())
        opensky_states_altitudes.append(row['altitude'].item())
        
    df_tracks = df_opensky_tracks.loc[(flight_id,), :]
    
    opensky_tracks_timestamps = []
    opensky_tracks_altitudes = []
    
    for seq, row in df_tracks.groupby(level='sequence'):
        opensky_tracks_timestamps.append(row['timestamp'].item())
        opensky_tracks_altitudes.append(row['baroAltitude'].item())
                
plt.plot(opensky_states_timestamps, opensky_states_altitudes, color=OPENSKY_STATES_ALTITUDES_COLOR, linewidth=4)
plt.plot(opensky_tracks_timestamps, opensky_tracks_altitudes, color=OPENSKY_ALTITUDES_COLOR, linewidth=4)

plt.savefig("vertical_profile_SAS410.png")

plt.gcf().clear() 

plt.figure(figsize=(9,6))
plt.xlabel('Longitude', fontsize=25)
plt.ylabel('Latitude', fontsize=25)

for flight_id, flight_id_group in df_opensky_states.groupby(level='flightId'):

    opensky_states_longitudes = []
    opensky_states_latitudes = []
    
    for seq, row in flight_id_group.groupby(level='sequence'):
        opensky_states_longitudes.append(row['lon'].item())
        opensky_states_latitudes.append(row['lat'].item())        
        
    df_tracks = df_opensky_tracks.loc[(flight_id,), :]
    
    opensky_tracks_longitudes = []
    opensky_tracks_latitudes = []
    
    for seq, row in df_tracks.groupby(level='sequence'):
        opensky_tracks_longitudes.append(row['lon'].item())
        opensky_tracks_latitudes.append(row['lat'].item())
        
plt.plot(opensky_states_longitudes, opensky_states_latitudes, color=OPENSKY_STATES_PLOT_COLOR, linewidth=1)
plt.plot(opensky_tracks_longitudes, opensky_tracks_latitudes, color=OPENSKY_PLOT_COLOR, marker='o', linewidth=1)

plt.savefig("horizontal_trajectory_SAS410.png")