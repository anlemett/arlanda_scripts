from datetime import datetime

#UTC time:
DATE_TIME_BEGIN = datetime(2018, 1, 1, 0, 0, 0, 0)
DATE_TIME_END = datetime(2018, 1, 7, 0, 0, 0, 0)

import pandas as pd

import requests
import time
import simplejson

TMA_timezone = "Europe/Stockholm"
airport_icao = "ESSA"

class LiveDataRetriever:
    API_URL = 'https://opensky-network.org/api'

    AUTH_DATA = ('tatianapolishchuk', 'q1w2e3r4')

    def get_list_of_arriving_aircraft(self, timestamp_begin, timestamp_end):

        arriving_flights_url = self.API_URL + '/flights/arrival'

        request_params = {
            'airport': airport_icao,
            'begin': timestamp_begin,
            'end': timestamp_end
        }

        res = requests.get(arriving_flights_url, params=request_params, auth=self.AUTH_DATA).json()

        return res


timestamp_begin = int(DATE_TIME_BEGIN.timestamp())   #float -> int
timestamp_end = int(DATE_TIME_END.timestamp())


opensky_filename = 'opensky_with_flight_ids' + DATE_TIME_BEGIN.strftime("_%Y_%m_%d") + DATE_TIME_END.strftime("_%Y_%m_%d") + '.csv'

opensky_df = pd.read_csv(opensky_filename, sep=' ',
                    index_col=[0,1],
                    dtype={"beginDate": str,  "date": str, "time": str})

ddr_df = pd.read_csv('ddr_m1.csv', sep=' ',
                    index_col=[0,1],
                    dtype={"beginTime": str, "endTime": str, "beginDate": str, "endDate": str, "flightId": int})

ddr_df = ddr_df[(ddr_df.beginTimestamp > timestamp_begin) & (ddr_df.beginTimestamp < timestamp_end)]


data_retriever = LiveDataRetriever()
flights = data_retriever.get_list_of_arriving_aircraft(timestamp_begin, timestamp_end)


ddr_number_of_flights = len(ddr_df.groupby(level='flightId'))
print(ddr_number_of_flights)

opensky_number_of_flights = len(flights)
print(opensky_number_of_flights)

opensky_with_flight_ids_number_of_flights = len(opensky_df.groupby(level='flightId'))
print(opensky_with_flight_ids_number_of_flights)
