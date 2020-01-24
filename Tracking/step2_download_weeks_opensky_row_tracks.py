import os

year = '2018'

OUTPUT_DIR = os.path.join("data", "tracks_opensky_downloaded_" + year)


from datetime import datetime
from datetime import timezone
import calendar

TMA_timezone = "Europe/Stockholm"
airport_icao = "ESSA"


import requests
#import simplejson
import math
import pandas as pd


from opensky_credentials import USERNAME, PASSWORD

class LiveDataRetriever:
    API_URL = 'https://opensky-network.org/api'

    AUTH_DATA = (USERNAME, PASSWORD)

    def get_list_of_arriving_aircraft(self, timestamp_begin, timestamp_end):

        arriving_flights_url = self.API_URL + '/flights/arrival'

        request_params = {
            'airport': airport_icao,
            'begin': timestamp_begin,
            'end': timestamp_end
        }

        res = requests.get(arriving_flights_url, params=request_params, auth=self.AUTH_DATA).json()

        return res

    def get_track_data(self, flight_icao24, flight_time):
        track_data_url = self.API_URL + '/tracks/all'

        request_params = {
            'time': flight_time,
            'icao24': flight_icao24
        }

        return requests.get(track_data_url, params=request_params, auth=self.AUTH_DATA).json()


# API does not allow longer than 7 days time periods
def get_tracks_data(data_retriever, flights, date_time_begin, date_time_end, month, week):

    number_of_flights = len(flights)

    new_data = []
    dropped_flights = 0

    for i in range(number_of_flights):
        print(month, week, number_of_flights, i)

        if flights[i] == 'Start after end time or more than seven days of data requested': #22.10.2018-29.10.2018 -> 28.10 to 5th week
            print(flights[i])
            continue

        if flights[i]['icao24'] is None:
            dropped_flights = dropped_flights + 1
            continue

        if flights[i]['firstSeen'] is None:
            dropped_flights = dropped_flights + 1
            continue

        if flights[i]['lastSeen'] is None:
            dropped_flights = dropped_flights + 1
            continue

        #d: icao24, startTime, endTime, callsign, path (time, latitude, longitude, baro_altitude, true_track, on_ground)
        try:
            d = data_retriever.get_track_data(flights[i]['icao24'], math.ceil((flights[i]['firstSeen']+flights[i]['lastSeen'])/2))
        except:
            dropped_flights = dropped_flights + 1
            continue

        sequence = 1
        for element in d['path']:
            new_d = {}

            new_d['origin'] = flights[i]['estDepartureAirport']

            new_d['sequence'] = sequence
            sequence = sequence + 1

            end_timestamp = d['endTime']
            end_datetime = datetime.utcfromtimestamp(end_timestamp)
            new_d['endDate'] = end_datetime.strftime('%y%m%d')

            el_timestamp = element[0]    #time
            el_datetime = datetime.utcfromtimestamp(el_timestamp)

            new_d['date'] = el_datetime.strftime('%y%m%d')
            new_d['time'] = el_datetime.strftime('%H%M%S')
            new_d['timestamp'] = el_timestamp
            new_d['lat'] = element[1]
            new_d['lon'] = element[2]
            new_d['baroAltitude'] = element[3]

            new_d['callsign'] = d['callsign'].strip() if d['callsign'] else ''
            new_d['icao24'] = d['icao24'].strip() if d['icao24'] else ''

            new_data.append(new_d)

    print("Dropped flights number:")
    print(dropped_flights)

    data_df = pd.DataFrame(new_data, columns = ['sequence', 'origin', 'endDate', 'callsign', 'icao24', 'date','time', 'timestamp', 'lat', 'lon', 'baroAltitude'])

    return data_df


def download_tracks_week(month, week, date_time_begin, date_time_end):
    
    timestamp_begin = int(date_time_begin.timestamp())   #float -> int
    timestamp_end = int(date_time_end.timestamp())

    data_retriever = LiveDataRetriever()
    flights = data_retriever.get_list_of_arriving_aircraft(timestamp_begin, timestamp_end)

    opensky_df = get_tracks_data(data_retriever, flights, date_time_begin, date_time_end, month, week)

    opensky_df = opensky_df.astype({"time": str, "date": str})
    opensky_df.reset_index(drop=True, inplace=True)
    
    filename = 'tracks_opensky_downloaded_' + year + '_' + month + '_week' + str(week) + '.csv'
    opensky_df.to_csv(os.path.join(OUTPUT_DIR, filename), sep=' ', encoding='utf-8', float_format='%.6f', header=None, index=False)
    

import time
start_time = time.time()

from multiprocessing import Process

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:
    
    procs = [] 
    
    for week in range(0,4):

        DATE_TIME_BEGIN = datetime(int(year), int(month), week * 7 + 1, 0, 0, 0, 0, timezone.utc)
        if month == '02' and not calendar.isleap(int(year)):
            DATE_TIME_END = datetime(int(year), 3, 1, 0, 0, 0, 0)
        else:
            DATE_TIME_END = datetime(int(year), int(month), (week + 1) * 7 + 1, 0, 0, 0, 0, timezone.utc)
            
        proc = Process(target=download_tracks_week, args=(month, week + 1, DATE_TIME_BEGIN, DATE_TIME_END,))
        procs.append(proc)
        proc.start()

    if month == '02' and not calendar.isleap(int(year)):
        continue
    elif month == '12':
        DATE_TIME_BEGIN = datetime(int(year), 12, 29, 0, 0, 0, 0, timezone.utc)
        DATE_TIME_END = datetime(int(year) + 1, 1, 1, 0, 0, 0, 0, timezone.utc)
    else:
        DATE_TIME_BEGIN = datetime(int(year), int(month), 29, 0, 0, 0, 0, timezone.utc)
        DATE_TIME_END = datetime(int(year), int(month) + 1, 1, 0, 0, 0, 0, timezone.utc)
    
    proc = Process(target=download_tracks_week, args=(month, 5, DATE_TIME_BEGIN, DATE_TIME_END,))
    procs.append(proc)
    proc.start()
    
    # complete the processes      
    for proc in procs:
        proc.join()
        
print((time.time()-start_time)/60)        
