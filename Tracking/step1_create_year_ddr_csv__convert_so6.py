import pandas as pd
from datetime import datetime

import os

year = '2018'

DDR_SO6_INPUT_DIR = os.path.join("data", "tracks_ddr_so6_" + year)

tracks_ddr_so6_m1_filename = os.path.join(DDR_SO6_INPUT_DIR, year + '_ESSA_arrivals_m1.so6')
tracks_ddr_so6_m3_filename = os.path.join(DDR_SO6_INPUT_DIR, year + '_ESSA_arrivals_m3.so6')

DDR_M1_OUTPUT_DIR = os.path.join("data", "tracks_ddr_m1_" + year)
tracks_ddr_m1_filename = os.path.join(DDR_M1_OUTPUT_DIR, 'tracks_ddr_m1_' + year + '.csv')

DDR_M3_OUTPUT_DIR = os.path.join("data", "tracks_ddr_m3_" + year)
tracks_ddr_m3_filename = os.path.join(DDR_M3_OUTPUT_DIR, 'tracks_ddr_m3_' + year + '.csv')


def getTimestamp(date, time):

    datetime_object = datetime.strptime(date+time, '%y%m%d%H%M%S')
    return int(datetime_object.timestamp())

def minuteDecimaleToDegree(latlon):
    #The following is the simple equation to convert degrees, minutes, and seconds into decimal degrees:
    #DD = (Seconds/3600) + (Minutes/60) + Degrees
    #The conversion must be handled differently if the degrees value is negative. Here's one way:
    #DD = - (Seconds/3600) - (Minutes/60) + Degrees (not implemented, not needed for arlanda)
    return float(latlon)/60

def flightLevelToAltitude(fl):
    return int(fl) * 30.48  # flight level -> feet -> meters


def create_ddr_m1():
    print("create ddr_m1")
    ddr_m1_df = pd.read_csv(tracks_ddr_so6_m1_filename, sep=' ', header=None,
                        names=['segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                        'beginFL', 'endFL', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                        'endLat', 'endLon', 'flightId', 'sequence', 'segmentLength', 'segmentParityColor'],
                        index_col=[16,17],
                        dtype={'flightId':int, 'sequence':int, 'beginTime':str, 'endTime':str, 'beginDate':str, 'endDate':str})

    print("beginTimestamp")
    ddr_m1_df['beginTimestamp'] = ddr_m1_df.apply(lambda row: getTimestamp(row['beginDate'], row['beginTime']), axis=1)
    print("endTimestamp")
    ddr_m1_df['endTimestamp'] = ddr_m1_df.apply(lambda row: getTimestamp(row['endDate'], row['endTime']), axis=1)

    print("beginLat")
    ddr_m1_df['beginLat'] = ddr_m1_df.apply(lambda row: minuteDecimaleToDegree(row['beginLat']), axis=1)
    print("beginLon")
    ddr_m1_df['beginLon'] = ddr_m1_df.apply(lambda row: minuteDecimaleToDegree(row['beginLon']), axis=1)
    print("endLat")
    ddr_m1_df['endLat'] = ddr_m1_df.apply(lambda row: minuteDecimaleToDegree(row['endLat']), axis=1)
    print("endLon")
    ddr_m1_df['endLon'] = ddr_m1_df.apply(lambda row: minuteDecimaleToDegree(row['endLon']), axis=1)

    print("beginFL")
    ddr_m1_df['beginFL'] = ddr_m1_df.apply(lambda row: flightLevelToAltitude(row['beginFL']), axis=1)
    print("endFL")
    ddr_m1_df['endFL'] = ddr_m1_df.apply(lambda row: flightLevelToAltitude(row['endFL']), axis=1)

    ddr_m1_df.to_csv(tracks_ddr_m1_filename, sep=' ', encoding='utf-8', float_format='%.6f', header=None)


def create_ddr_m3():
    print("create ddr_m3")
    ddr_m3_df = pd.read_csv(tracks_ddr_so6_m3_filename, sep=' ', header=None,
                        names=['segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                        'beginFL', 'endFL', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                        'endLat', 'endLon', 'flightId', 'sequence', 'segmentLength', 'segmentParityColor'],
                        index_col=[16,17],
                        dtype={'flightId':int, 'sequence':int, 'beginTime':str, 'endTime':str, 'beginDate':str, 'endDate':str})

    print("beginTimestamp")
    ddr_m3_df['beginTimestamp'] = ddr_m3_df.apply(lambda row: getTimestamp(row['beginDate'], row['beginTime']), axis=1)
    print("endTimestamp")
    ddr_m3_df['endTimestamp'] = ddr_m3_df.apply(lambda row: getTimestamp(row['endDate'], row['endTime']), axis=1)

    print("beginLat")
    ddr_m3_df['beginLat'] = ddr_m3_df.apply(lambda row: minuteDecimaleToDegree(row['beginLat']), axis=1)
    print("beginLon")
    ddr_m3_df['beginLon'] = ddr_m3_df.apply(lambda row: minuteDecimaleToDegree(row['beginLon']), axis=1)
    print("endLat")
    ddr_m3_df['endLat'] = ddr_m3_df.apply(lambda row: minuteDecimaleToDegree(row['endLat']), axis=1)
    print("endLon")
    ddr_m3_df['endLon'] = ddr_m3_df.apply(lambda row: minuteDecimaleToDegree(row['endLon']), axis=1)

    print("beginFL")
    ddr_m3_df['beginFL'] = ddr_m3_df.apply(lambda row: flightLevelToAltitude(row['beginFL']), axis=1)
    print("endFL")
    ddr_m3_df['endFL'] = ddr_m3_df.apply(lambda row: flightLevelToAltitude(row['endFL']), axis=1)

    ddr_m3_df.to_csv(tracks_ddr_m3_filename, sep=' ', encoding='utf-8', float_format='%.6f', header=None)

import time
start_time = time.time()

create_ddr_m1()
create_ddr_m3()

print((time.time()-start_time)/60)
