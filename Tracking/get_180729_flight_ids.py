import pandas as pd

import os

import time
start_time = time.time()

year = '2018'

DATA_DIR = os.path.join("data", "statistics_opensky_" + year)

input_filename = "statistics_opensky_by_flight_" + year + ".csv"

flight_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'date': str})

flight_df.set_index(['date'], inplace=True)


day_df = flight_df.loc['180729']

day_df.set_index(['hour'], inplace=True)

#print(day_df.head())

print(day_df.loc[6]['flight_id'])