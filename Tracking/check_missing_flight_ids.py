import pandas as pd
import numpy as np

from constants import *


import os

year = "2018"

DATA_DIR = "data"



missingIds = []

INPUT_DIR = os.path.join(DATA_DIR, "tracks_ddr_m1_" + year)
filename = os.path.join(INPUT_DIR, 'tracks_ddr_m1_' + year + '.csv')

df = pd.read_csv(filename, sep=' ',
                    names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                           'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                           'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                     index_col=[0,1],
                     dtype={'flightId':str, 'sequence':int, 'segmentId': str,  'beginTime':str, 'endTime':str, 'beginDate':str, 'endDate':str})
    

frames = []

for id in missingIds:
    flight_df = df.loc([id,])
   
missing_df = pd.concat(frames)

missing_df.reset_index(inplace=True)
missing_df.to_csv("missing_ddr_m1.csv", sep=' ', encoding='utf-8', header=None, index=False)


