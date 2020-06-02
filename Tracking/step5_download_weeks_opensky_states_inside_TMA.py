from datetime import datetime

import os

year = "2018"

DATA_DIR = "data"
DATA_INPUT_DIR = os.path.join(DATA_DIR, "tracks_TMA_opensky_" + year)
DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "states_TMA_opensky_downloaded_" + year)


from opensky_credentials import USERNAME, PASSWORD

import paramiko
from io import StringIO
import re

import numpy as np
import pandas as pd
import calendar

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from constants import *


def get_df(impala_log, time_end):
    s = StringIO()
    count = 0
    for line in impala_log.readlines():
        line = line.strip()
        if re.match("\|.*\|", line):
            count += 1
            s.write(re.sub(" *\| *", ",", line)[1:-2])
            s.write("\n")

    #contents = s.getvalue()
    #print(contents)
    
    if count > 0:
        s.seek(0)
        df = pd.read_csv(s, sep=',', error_bad_lines=False, warn_bad_lines=True)
        df = df.fillna(0)
        df.index = df.index.set_names(['sequence'])
        df.columns = ['timestamp', 'lat', 'lon', 'altitude', 'velocity']
        df[['lat', 'lon']] = df[['lat', 'lon']].apply(pd.to_numeric, downcast='float', errors='coerce').fillna(0)
        df[['altitude', 'velocity']] = df[['altitude', 'velocity']].apply(pd.to_numeric, downcast='integer', errors='coerce').fillna(0)
        df['altitude'] = df['altitude'].astype(int)
        df['velocity'] = df['velocity'].astype(int)
        end_datetime = datetime.utcfromtimestamp(time_end)
        df['endDate'] = end_datetime.strftime('%y%m%d')

        df.reset_index(level=df.index.names, inplace=True)
        return df

#Set in this function which fields to extract (in sql request)
def request_states(icao24, time_begin, time_end):
    time_begin_datetime = datetime.fromtimestamp(time_begin)
    hour_datetime = time_begin_datetime.replace(microsecond=0,second=0,minute=0)
    hour = int(datetime.timestamp(hour_datetime))

    time_begin_str = str(time_begin)
    time_end_str = str(time_end)
    hour_str = str(hour)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        try:
            client.connect(
                hostname = 'data.opensky-network.org',
                port=2230,
                username=USERNAME,
                password=PASSWORD,
                timeout=60,
                look_for_keys=False,
                allow_agent=False,
                #compress=True
                )
            break
        except paramiko.SSHException as err:
            print(err)
            time.sleep(2)
        except:
            print("exception")
            time.sleep(2)

    shell = client.invoke_shell()

    total = ""
    while len(total) == 0 or total[-10:] != ":21000] > ":
        b = shell.recv(256)
        total += b.decode()

    request = "select time, lat, lon, baroaltitude, velocity from state_vectors_data4 where icao24=\'" + icao24 + "\' and time>=" + time_begin_str + " and time<=" + time_end_str + " and hour=" + hour_str +";\n"
    #print(request)
    shell.send(request)
    total = ""
    while len(total) == 0 or total[-10:] != ":21000] > ":
        b = shell.recv(256)
        total += b.decode()

    impala_log = StringIO(total)

    shell.close()
    client.close()
    return get_df(impala_log, time_end)


def get_entry_point_index(flight_id, new_df):
    for seq, row in new_df.groupby(level='sequence'):
        lon = row.loc[(flight_id, seq)]['lon']
        lat = row.loc[(flight_id, seq)]['lat']

        if (check_TMA_contains_point(Point(lon, lat))):
            return seq
    return 0


def check_TMA_contains_point(point):

    lons_lats_vect = np.column_stack((TMA_lon, TMA_lat)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon

    return polygon.contains(point)


def download_states_week(month, week):
    
    # opensky tracks csv
    opensky_tracks_filename = 'tracks_TMA_opensky_' + year + '_' + month + '_week' + str(week) + '.csv'

    #opensky states inside TMA csv
    opensky_states_filename = 'states_TMA_opensky_downloaded_' + year + '_' + month + '_week' + str(week) + '.csv'

    opensky_states_df = pd.DataFrame()

    opensky_tracks_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, opensky_tracks_filename), sep=' ',
                                names=['flightId', 'sequence', 'beginDate', 'callsign', 'icao24', 'date', 'time', 'timestamp',
                                    'lat', 'lon', 'baroAltitude', 'aircraftType', 'origin'],
                                index_col=[0,1],
                                dtype={'flightId':int, 'sequence':int, 'icao24': str, 'timestamp':int})


    number_of_flights = len(opensky_tracks_df.groupby(level='flightId'))

    count = 0

    for flight_id, new_df in opensky_tracks_df.groupby(level='flightId'):
        count = count + 1
    
        print(month, week, number_of_flights, count)
    
        (id, last_index) = new_df.index[-1]

        entry_point_index = get_entry_point_index(flight_id, new_df)

        if entry_point_index == 0:
            continue

        icao24 = new_df.loc[(flight_id, entry_point_index)]['icao24']
        time_begin = new_df.loc[(flight_id, entry_point_index)]['timestamp']
        time_end = new_df.loc[(flight_id, last_index)]['timestamp']

        flight_id_states_df = request_states(icao24, time_begin, time_end)

        if flight_id_states_df is not None and not flight_id_states_df.empty:

            flight_id_states_df.insert(0, 'flight_id', flight_id)
            flight_id_states_df.set_index(['flight_id', 'sequence'], inplace=True)

            opensky_states_df = pd.concat([opensky_states_df, flight_id_states_df], axis=0, sort=False)
            opensky_states_df.to_csv(os.path.join(DATA_OUTPUT_DIR, opensky_states_filename), sep=' ', encoding='utf-8', float_format='%.3f', header=None)

 
import time
start_time = time.time()

from multiprocessing import Process

#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
months = ['05', '06', '07', '08', '09', '10', '11', '12']

for month in months:

    procs = [] 
        
    number_of_weeks = (5, 4)[month == '02' and not calendar.isleap(int(year))]
        
    for week in range(0, number_of_weeks):
        
        proc = Process(target=download_states_week, args=(month, week + 1,))
        procs.append(proc)
        proc.start()
        #download_states_week(month, week + 1)
        
    # complete the processes      
    for proc in procs:
        proc.join()

print((time.time()-start_time)/60)
