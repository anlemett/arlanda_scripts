from datetime import datetime
from datetime import timezone

import time
start_time = time.time()


year = "2018"

#UTC time:
DATE_TIME_BEGIN = datetime(2018, 1, 1, 0, 0, 0, 0, timezone.utc)
DATE_TIME_END = datetime(2018, 1, 2, 0, 0, 0, 0, timezone.utc)

from opensky_credentials import USERNAME, PASSWORD

# opensky tracks csv
opensky_filename = 'opensky_with_flight_ids' + DATE_TIME_BEGIN.strftime("_%Y_%m_%d") + DATE_TIME_END.strftime("_%Y_%m_%d") + '.csv'

#opensky states inside TMA csv
opensky_states_filename = 'opensky_states_SAS410_1_01.csv'

import paramiko
from io import StringIO
import re

import numpy as np
import pandas as pd

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from constants import *

import time
start_time = time.time()


def get_df(impala_log, time_begin):
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
        df.index = df.index.set_names(['sequence'])
        df.columns = ['timestamp', 'callsign', 'lat', 'lon', 'altitude', 'velocity']
        df[['lat', 'lon']] = df[['lat', 'lon']].apply(pd.to_numeric, downcast='float', errors='coerce').fillna(0)
        df['altitude'] = df['altitude'].astype(int)
        df['velocity'] = df['velocity'].astype(int)
        begin_datetime = datetime.utcfromtimestamp(time_begin)
        df['beginDate'] = begin_datetime.strftime('%y%m%d')

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

    request = "select time, callsign, lat, lon, baroaltitude, velocity from state_vectors_data4 where icao24=\'" + icao24 + "\' and time>=" + time_begin_str + " and time<=" + time_end_str + " and hour=" + hour_str +";\n"
    #print(request)
    shell.send(request)
    total = ""
    while len(total) == 0 or total[-10:] != ":21000] > ":
        b = shell.recv(256)
        total += b.decode()

    impala_log = StringIO(total)

    shell.close()
    client.close()
    return get_df(impala_log, time_begin)


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


opensky_states_df = pd.DataFrame()

opensky_tracks_df = pd.read_csv(opensky_filename, sep=' ',
                                names=['flightId', 'sequence', 'beginDate', 'callsign', 'icao24', 'date', 'time', 'timestamp',
                                    'lat', 'lon', 'baroAltitude', 'aircraftType', 'origin'],
                                index_col=[0,1],
                                dtype={'flightId':int, 'sequence':int, 'icao24': str, 'timestamp':int, 'baroAltitude': int})


number_of_flights = len(opensky_tracks_df.groupby(level='flightId'))
print(number_of_flights)
count = 0

for flight_id, new_df in opensky_tracks_df.groupby(level='flightId'):
    count = count + 1
    
    #print(number_of_flights, count)
    
    if not flight_id==214186904:
        continue
    
    print(flight_id)
    
    l = len(new_df.index)

    entry_point_index = get_entry_point_index(flight_id, new_df)

    print(entry_point_index)
    
    if entry_point_index == 0:
        continue

    icao24 = new_df.loc[(flight_id, entry_point_index)]['icao24']
    print(icao24)
    time_begin = new_df.loc[(flight_id, entry_point_index)]['timestamp']
    print(time_begin)
    time_end = new_df.loc[(flight_id, l)]['timestamp']
    print(time_end)

    flight_id_states_df = request_states(icao24, time_begin, time_end)
    #print(flight_id_states_df)

    if flight_id_states_df is not None and not flight_id_states_df.empty:
        
        flight_id_states_df.insert(0, 'flight_id', flight_id)
        flight_id_states_df.set_index(['flight_id', 'sequence'], inplace=True)
        
        opensky_states_df = pd.concat([opensky_states_df, flight_id_states_df], axis=0, sort=False)
        opensky_states_df.to_csv(opensky_states_filename, sep=' ', encoding='utf-8', float_format='%.4f', header=None)

print((time.time()-start_time)/60)
