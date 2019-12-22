import pandas as pd
import numpy as np

from constants import *


import os

year = "2018"

DATA_DIR = "data"


def get_enroute_tracks_year(is_m1):
    
    if is_m1:
        INPUT_DIR = os.path.join(DATA_DIR, "tracks_ddr_m1_" + year)
        filename = os.path.join(INPUT_DIR, 'tracks_ddr_m1_' + year + '.csv')
    else:
        INPUT_DIR = os.path.join(DATA_DIR, "tracks_ddr_m3_" + year)
        filename = os.path.join(INPUT_DIR, 'tracks_ddr_m3_' + year + '.csv')


    df = pd.read_csv(filename, sep=' ',
                    names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                           'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                           'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                    dtype=str)
    

    flightIdList = df.flightId.unique()
    print(flightIdList)
    
    df = pd.DataFrame()
    
    return flightIdList
    


def get_tma_tracks_year(is_m1):
    
    if is_m1:
        INPUT_DIR = os.path.join(DATA_DIR, "tracks_TMA_ddr_m1_" + year)
        filename = os.path.join(INPUT_DIR, 'tracks_TMA_ddr_m1_' + year + '.csv')
    else:
        INPUT_DIR = os.path.join(DATA_DIR, "tracks_TMA_ddr_m3_" + year)
        filename = os.path.join(INPUT_DIR, 'tracks_TMA_ddr_m3_' + year + '.csv')


    df = pd.read_csv(filename, sep=' ',
                    names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                           'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                           'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                     dtype=str)
                    
    
    flightIdList = df.flightId.unique()
    print(flightIdList)
    
    df = pd.DataFrame()
    
    return flightIdList

 
    
import time
time_start = time.time()

enrouteFlightIdList = get_enroute_tracks_year(True)
TMAFlightIdList = get_tma_tracks_year(True)


print(len(TMAFlightIdList))
print(len(enrouteFlightIdList))

a = set(enrouteFlightIdList)
b = set(TMAFlightIdList)

c = a.difference(b)
print(c)


print((time.time()-time_start)/60)
