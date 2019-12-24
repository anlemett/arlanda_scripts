import pandas as pd
import os

import time
start_time = time.time()

year = '2018'

DATA_DIR = "data"
OUTPUT_DIR = os.path.join(DATA_DIR, "statistics_ddr_" + year)


DDR_M1_CSV = os.path.join(os.path.join(DATA_DIR, "tracks_ddr_m1_" + year), "tracks_ddr_m1_" + year + ".csv")
DDR_M3_CSV = os.path.join(os.path.join(DATA_DIR, "tracks_ddr_m3_" + year), "tracks_ddr_m3_" + year + ".csv")
TMA_DDR_M1_CSV = os.path.join(os.path.join(DATA_DIR, "tracks_TMA_ddr_m1_" + year), "tracks_TMA_ddr_m1_" + year + ".csv")
TMA_DDR_M3_CSV = os.path.join(os.path.join(DATA_DIR, "tracks_TMA_ddr_m3_" + year), "tracks_TMA_ddr_m3_" + year + ".csv")


def get_all_tracks(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names=['flightId', 'sequence', 'segmentId', 'origin', 'destination', 'aircraftType', 'beginTime', 'endTime',
                           'beginAltitude', 'endAltitude', 'status', 'callsign', 'beginDate', 'endDate', 'beginLat', 'beginLon',
                           'endLat', 'endLon', 'segmentLength', 'segmentParityColor', 'beginTimestamp', 'endTimestamp'],
                     index_col=[0,1],
                     dtype={'flightId':int, 'endDate':str, 'endTime':str, 'beginTimestamp':int, 'endTimestamp':int})
    return df


m1_df = get_all_tracks(DDR_M1_CSV)
m3_df = get_all_tracks(DDR_M3_CSV)

m1_by_flight_df = pd.DataFrame(columns=['flight_id', 'endDate', 'endTime', 'beginTimestamp', 'endTimestamp'])
m3_by_flight_df = pd.DataFrame(columns=['flight_id', 'endDate', 'endTime', 'beginTimestamp', 'endTimestamp'])

print("m1 processing")
m1_flight_id_num = len(m1_df.groupby(level='flightId'))
print("m1", m1_flight_id_num)

count = 1
for id, new_df in m1_df.groupby(level='flightId'):
    print("m1", m1_flight_id_num, count)
    count = count + 1
        
    begin_timestamp = new_df['beginTimestamp'].values[0]
    end_timestamp = new_df['endTimestamp'].values[-1]
    endDate = new_df['endDate'].values[-1]
    endTime = new_df['endTime'].values[-1]
    m1_by_flight_df = m1_by_flight_df.append({'flight_id': id, 'endDate':  endDate, 'endTime': endTime,
                                              'beginTimestamp': begin_timestamp, 'endTimestamp': end_timestamp}, ignore_index=True)

print("m3 processing")
m3_flight_id_num = len(m3_df.groupby(level='flightId'))
print("m3", m3_flight_id_num)

count = 1
for id, new_df in m3_df.groupby(level='flightId'):
    print("m3", m3_flight_id_num, count)
    count = count + 1
        
    begin_timestamp = new_df['beginTimestamp'].values[0]
    end_timestamp = new_df['endTimestamp'].values[-1]
    endDate = new_df['endDate'].values[-1]
    end_time = new_df['endTime'].values[-1]
    m3_by_flight_df = m3_by_flight_df.append({'flight_id': id, 'endDate':  endDate, 'endTime': endTime,
                                              'beginTimestamp': begin_timestamp, 'endTimestamp': end_timestamp}, ignore_index=True)

print("ddr stat")

stat_by_flight_df = pd.merge(m1_by_flight_df, m3_by_flight_df, on=['flight_id'], suffixes=["_L", "_R"])
stat_by_flight_df['departure_delay'] = stat_by_flight_df['beginTimestamp_R'] - stat_by_flight_df['beginTimestamp_L']
stat_by_flight_df['arrival_delay'] = stat_by_flight_df['endTimestamp_R'] - stat_by_flight_df['endTimestamp_L']
stat_by_flight_df['enroute_delay'] = (stat_by_flight_df['endTimestamp_R'] - stat_by_flight_df['beginTimestamp_R']) -\
    (stat_by_flight_df['endTimestamp_L'] - stat_by_flight_df['beginTimestamp_L'])
stat_by_flight_df['endDate'] = stat_by_flight_df['endDate_L']
stat_by_flight_df['endTime'] = stat_by_flight_df['endTime_L']
stat_by_flight_df = stat_by_flight_df[['endDate', 'endTime', 'flight_id', 'departure_delay', 'arrival_delay', 'enroute_delay']]
stat_by_flight_df.reset_index(drop=True, inplace=True)
  

TMA_m1_df = get_all_tracks(TMA_DDR_M1_CSV)
TMA_m3_df = get_all_tracks(TMA_DDR_M3_CSV)

TMA_m1_by_flight_df = pd.DataFrame(columns=['flight_id', 'TMA_time'])
TMA_m3_by_flight_df = pd.DataFrame(columns=['flight_id', 'TMA_time'])

print("TMA m1 processing")
TMA_m1_flight_id_num = len(TMA_m1_df.groupby(level='flightId'))
print("TMA_m1", TMA_m1_flight_id_num)

count = 1
for id, new_df in TMA_m1_df.groupby(level='flightId'):
    print("TMA_m1", TMA_m1_flight_id_num, count)
    count = count + 1
        
    begin_timestamp = new_df['beginTimestamp'].values[0]
    end_timestamp = new_df['endTimestamp'].values[-1]
    TMA_time = end_timestamp - begin_timestamp
    TMA_m1_by_flight_df = TMA_m1_by_flight_df.append({'flight_id': id, 'TMA_time': TMA_time}, ignore_index=True)

print("TMA m3 processing")
TMA_m3_flight_id_num = len(TMA_m3_df.groupby(level='flightId'))
print(TMA_m3_flight_id_num)

count = 1
for id, new_df in TMA_m3_df.groupby(level='flightId'):
    print("TMA_m3", TMA_m1_flight_id_num, count)
    count = count + 1
    
    begin_time = new_df['beginTimestamp'].values[0].item(0)
    end_time = new_df['endTimestamp'].values[-1].item(0)
    TMA_time = end_time - begin_time
    TMA_m3_by_flight_df = TMA_m3_by_flight_df.append({'flight_id': id, 'TMA_time': TMA_time}, ignore_index=True)

print("TMA ddr stat")

TMA_stat_by_flight_df = pd.merge(TMA_m1_by_flight_df, TMA_m3_by_flight_df, on=['flight_id'], suffixes=["_L", "_R"])
TMA_stat_by_flight_df['add_time'] = TMA_stat_by_flight_df['TMA_time_R'] - TMA_stat_by_flight_df['TMA_time_L']
TMA_stat_by_flight_df = TMA_stat_by_flight_df[['flight_id', 'add_time']]
TMA_stat_by_flight_df.reset_index(drop=True, inplace=True)
    

print("merging stat")
#merging ddr stat and TMA ddr stat
ddr_stat_by_flight_df = pd.merge(stat_by_flight_df, TMA_stat_by_flight_df, on=['flight_id'])
ddr_stat_by_flight_df.reset_index(drop=True, inplace=True)
    
filename = "statistics_ddr_by_flight_" + year + ".csv"
ddr_stat_by_flight_df.to_csv(os.path.join(OUTPUT_DIR, filename), sep=' ', encoding='utf-8', float_format='%.6f', header=None)

print("--- %s minutes ---" % ((time.time() - start_time)/60))