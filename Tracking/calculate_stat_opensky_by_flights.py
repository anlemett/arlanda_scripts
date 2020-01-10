import pandas as pd
import os

from datetime import datetime

import time
start_time = time.time()

year = '2018'

DATA_INPUT_DIR = os.path.join("data", "states_TMA_opensky_merged_with_ddr_m3_" + year)
input_filename = "states_TMA_opensky_" + year + ".csv"
DATA_OUTPUT_DIR = os.path.join("data", "statistics_opensky_" + year)
output_filename = "statistics_opensky_by_flight_" + year + ".csv"


def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'velocity', 'endDate', 'aircraftType'],
                    dtype={'flightId':int, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'altitude':float, 'velocity':float, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'altitude', 'velocity', 'endDate']]
    
    df.set_index(['flightId', 'sequence'], inplace=True)

    return df


def calculate_vfe(states_opensky_df, full_vfe_csv_filename):
    min_level_time = 30
    #Y/X = 300 feet per minute
    rolling_window_Y = (300*(min_level_time/60))/ 3.281 # feet to meters
    #print(rolling_window_Y)

    #descent part ends at 1800 feet
    descent_end_altitude = 1800 / 3.281
    #print(descent_end_altitude)

    vfe_df = pd.DataFrame(columns=['flight_id', 'date', 'hour', 'number_of_levels', 'time_on_levels', 'time_on_levels_percent',
                                   'distance_on_levels', 'distance_on_levels_percent'])


    number_of_levels_lst = []
    distance_on_levels_lst = []
    distance_on_levels_percent_lst = []
    time_on_levels_lst = []
    time_on_levels_percent_lst = []

    flight_id_num = len(states_opensky_df.groupby(level='flightId'))
    number_of_level_flights = 0

    count = 0
    for flight_id, flight_id_group in states_opensky_df.groupby(level='flightId'):
        
        count = count + 1
        print(flight_id_num, count, flight_id)

        number_of_levels = 0

        time_sum = 0
        time_on_levels = 0
        time_on_level = 0

        distance_sum = 0
        distance_on_levels = 0
        distance_on_level = 0

        level = 'false'
        altitude1 = 0 # altitude at the beginning of rolling window
        altitude2 = 0 # altitude at the end of rolling window

        seq_level_end = 0
        seq_min_level_time = 0

        df_length = len(flight_id_group)
        for seq, row in flight_id_group.groupby(level='sequence'):

            if (seq + min_level_time) >= df_length:
                break

            #print("row", row) 
            #print("row[altitude]", row['altitude'])
            altitude1 = row['altitude'].values[0]

            altitude2 = flight_id_group.loc[flight_id, seq+min_level_time-1]['altitude']
                    
            #print('altitude1', altitude1)
            #print('altitude2', altitude2)

            if altitude2 < descent_end_altitude:
                break

            time_sum = time_sum + 1
            distance_sum = distance_sum + row['velocity'].values[0]

            if abs(altitude1 - altitude2) > 1000:
                continue

            if level == 'true':

                if seq < seq_level_end:
                    if altitude1 - altitude2 < rolling_window_Y: #extend the level
                        seq_level_end = seq_level_end + 1
                    if seq < seq_min_level_time: # do not count first 30 seconds
                        continue
                    else:
                        time_on_level = time_on_level + 1
                        distance_on_level = distance_on_level + row['velocity'].values[0]
                else: # level ends
                    if seq_level_end >= seq_min_level_time:
                        number_of_levels = number_of_levels + 1
                    level = 'false'
                    time_on_levels = time_on_levels + time_on_level
                    distance_on_levels = distance_on_levels + distance_on_level
                    time_on_level = 0
                    distance_on_level = 0
            else: #not level
                if altitude1 - altitude2 < rolling_window_Y: # level begins
                    level = 'true'
                    seq_min_level_time = seq + min_level_time
                    seq_level_end = seq + min_level_time - 1
                    time_on_level = time_on_level + 1
                    distance_on_level = distance_on_level + row['velocity'].values[0]

        if (time_sum == 0) or (distance_sum == 0):
            print(type(time_sum))
            print(type(distance_sum))
            
            continue
        if number_of_levels > 0:
            number_of_level_flights = number_of_level_flights + 1
        number_of_levels_str = str(number_of_levels)

        number_of_levels_lst.append(number_of_levels)

        # convert distance to NM and time to munutes
        distance_on_levels = distance_on_levels * 0.000539957   #meters to NM
        distance_sum = distance_sum * 0.000539957   #meters to NM
        time_on_levels = time_on_levels / 60    #seconds to minutes
        time_sum = time_sum /60   #seconds to minutes

        distance_on_levels_lst.append(distance_on_levels)
        distance_on_levels_str = "{0:.3f}".format(distance_on_levels)

        distance_on_levels_percent = distance_on_levels / distance_sum *100
        distance_on_levels_percent_lst.append(distance_on_levels_percent)
        distance_on_levels_percent_str = "{0:.1f}".format(distance_on_levels_percent)


        time_on_levels_lst.append(time_on_levels)
        time_on_levels_str = "{0:.3f}".format(time_on_levels)

        time_on_levels_percent = time_on_levels / time_sum *100
        time_on_levels_percent_lst.append(time_on_levels_percent)
        time_on_levels_percent_str = "{0:.1f}".format(time_on_levels_percent)

        date_str = states_opensky_df.loc[flight_id].head(1)['endDate'].values[0]
        
        #end_timestamp = states_opensky_df.loc[flight_id]['timestamp'].values[-1].item(0)
        end_timestamp = states_opensky_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        
        
        #print(date_str)
        #print(number_of_levels_str)
        #print(distance_on_levels_str)
        #print(distance_on_levels_percent_str)
        #print(time_on_levels_str)
        #print(time_on_levels_percent_str)
        vfe_df = vfe_df.append({'flight_id': flight_id, 'date': date_str, 'hour': end_hour_str, 'number_of_levels': number_of_levels_str,
                                'distance_on_levels': distance_on_levels_str, 'distance_on_levels_percent': distance_on_levels_percent_str,
                                'time_on_levels': time_on_levels_str, 'time_on_levels_percent': time_on_levels_percent_str}, ignore_index=True)

    vfe_df.to_csv(full_vfe_csv_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)



states_df = get_all_states(os.path.join(DATA_INPUT_DIR, input_filename))


full_stat_csv_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

#number_of_flights = len(states_df.index.get_level_values('flightId').unique())
number_of_flights = len(states_df.groupby(level='flightId'))

calculate_vfe(states_df, full_stat_csv_filename)

print("--- %s minutes ---" % ((time.time() - start_time)/60))