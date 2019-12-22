import pandas as pd
import os

import time
start_time = time.time()

year = '2018'

DATA_INPUT_DIR = os.path.join("data", "states_TMA_opensky_" + year)
input_filename = "states_TMA_opensky_" + year + ".csv"
DATA_OUTPUT_DIR = os.path.join("data", "statistics_opensky_" + year)
output_filename = "statistics_opensky_by_flight_" + year + ".csv"


def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ', index_col=[0,1],
                    names = ['flightId', 'sequence', 'altitude', 'velocity', 'beginDate'],
                    dtype={'flightId':int, 'sequence':int, 'altitude':float, 'velocity':float, 'beginDate':str})

    return df


def calculate_vfe(states_opensky_df, full_vfe_csv_filename):
    min_level_time = 30
    #Y/X = 300 feet per minute
    rolling_window_Y = (300*(min_level_time/60))/ 3.281 # feet to meters
    #print(rolling_window_Y)

    #descent part ends at 1800 feet
    descent_end_altitude = 1800 / 3.281
    #print(descent_end_altitude)

    vfe_df = pd.DataFrame(columns=['flight_id', 'date', 'number_of_levels', 'time_on_levels', 'time_on_levels_percent',
                                   'distance_on_levels', 'distance_on_levels_percent'])

    #states_opensky_df.reset_index(level=states_opensky_df.index.names, inplace=True)

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
        print(flight_id_num, count)

        #flight_id_states_df.set_index(['sequence'], inplace=True)

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
        altitude_level_begin = 0 #not used
        altitude_level_end = 0   #can be removed

        seq_level_begin = 0
        seq_level_end = 0
        seq_min_level_time = 0

        df_length = len(flight_id_group)
        for seq, row in flight_id_group.groupby(level='sequence'):

            if (seq + min_level_time) >= df_length:
                break

            altitude1 = row['altitude'].item()
            altitude2 = flight_id_group.loc[flight_id, seq+min_level_time-1]['altitude'].item()

            if altitude2 < descent_end_altitude:
                break

            time_sum = time_sum + 1
            distance_sum = distance_sum + row['velocity'].item()

            if abs(altitude1 - altitude2) > 1000:
                continue

            if level == 'true':

                if seq < seq_level_end:
                    if altitude1 - altitude2 < rolling_window_Y: #extend the level
                        seq_level_end = seq_level_end + 1
                        altitude_level_end = altitude2
                    if seq < seq_min_level_time: # do not count first 30 seconds
                        continue
                    else:
                        time_on_level = time_on_level + 1
                        distance_on_level = distance_on_level + row['velocity'].item()
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
                    seq_level_begin = seq
                    seq_min_level_time = seq + min_level_time
                    seq_level_end = seq + min_level_time - 1
                    altitude_level_begin = altitude1
                    altitude_level_end = altitude2
                    time_on_level = time_on_level + 1
                    distance_on_level = distance_on_level + row['velocity'].item()

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

        date_str = states_opensky_df.loc[flight_id].head(1)['beginDate'].item()
        
        print(date_str)
        print(number_of_levels_str)
        print(distance_on_levels_str)
        print(distance_on_levels_percent_str)
        print(time_on_levels_str)
        print(time_on_levels_percent_str)
        vfe_df = vfe_df.append({'flight_id': flight_id, 'date': date_str, 'number_of_levels': number_of_levels_str,
                                'distance_on_levels': distance_on_levels_str, 'distance_on_levels_percent': distance_on_levels_percent_str,
                                'time_on_levels': time_on_levels_str, 'time_on_levels_percent': time_on_levels_percent_str}, ignore_index=True)

    vfe_df.to_csv(full_vfe_csv_filename, sep=' ', encoding='utf-8', float_format='%.1f', header=True, index=False)



states_df = get_all_states(os.path.join(DATA_INPUT_DIR, input_filename))


full_stat_csv_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)

number_of_flights = len(states_df.index.get_level_values('flightId').unique())

calculate_vfe(states_df, full_stat_csv_filename)

print("--- %s minutes ---" % ((time.time() - start_time)/60))