import pandas as pd
import numpy as np
import os

import time
start_time = time.time()

year = '2018'

DATA_DIR = os.path.join("data", "statistics_ddr_" + year)



filename = "statistics_ddr_by_flight_" + year + ".csv"

ddr_by_flight_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
                               names = ['endDate', 'endTime', 'flight_id', 'departure_delay', 'arrival_delay', 'enroute_delay', 'add_time'],
                               index_col=[0],
                               dtype={'flightId':int, 'endDate':str, 'endTime':str, 'departure_delay':int, 'arrival_delay':int, 'enroute_delay':int, 'add_time':int})

ddr_by_flight_df.set_index(['endDate'], inplace=True)

ddr_by_day_df = pd.DataFrame(columns=['endDate', 'number_of_flights',
                                      'arrival_delayed_15_min_flights_number',
                                      'enroute_delayed_15_min_flights_number',
                                      'total_departure_delay', 'average_departure_delay', 'total_arrival_delay', 'average_arrival_delay',
                                      'total_enroute_delay', 'average_enroute_delay',
                                      'total_add_time_TMA', 'average_add_time_TMA'])

days_num = len(ddr_by_flight_df.groupby(level='endDate'))
print(days_num)

count = 1
for date, new_df in ddr_by_flight_df.groupby(level='endDate'):
    print(count)
    count = count + 1

    number_of_flights = len(new_df)
    
    arrival_delayed_15_min_df = new_df.loc[new_df.arrival_delay > 900, 'arrival_delay']
    arrival_delayed_15_min = len (arrival_delayed_15_min_df)

    enroute_delayed_15_min_df = new_df.loc[new_df.enroute_delay > 900, 'enroute_delay']
    enroute_delayed_15_min = len (enroute_delayed_15_min_df)

    departure_delays = new_df.loc[new_df.departure_delay > 0, 'departure_delay']
    ddr_total_departure_delay = int(np.sum(departure_delays)) if departure_delays.any() else 0
    ddr_average_departure_delay = int(ddr_total_departure_delay/number_of_flights) if departure_delays.any() else 0

    arrival_delays = new_df.loc[new_df.arrival_delay > 0, 'arrival_delay']
    ddr_total_arrival_delay = int(np.sum(arrival_delays)) if arrival_delays.any() else 0
    ddr_average_arrival_delay = int(ddr_total_arrival_delay/number_of_flights) if arrival_delays.any() else 0

    enroute_delays = new_df.loc[new_df.enroute_delay > 0, 'enroute_delay']
    ddr_total_enroute_delay = int(np.sum(enroute_delays)) if enroute_delays.any() else 0
    print(ddr_total_enroute_delay)
    ddr_average_enroute_delay = int(ddr_total_enroute_delay/number_of_flights) if enroute_delays.any() else 0

    add_times = new_df.loc[new_df.add_time > 0, 'add_time']
    ddr_total_add_times = int(np.sum(add_times)) if add_times.any() else 0
    ddr_average_add_time = int(ddr_total_add_times/number_of_flights) if add_times.any() else 0


    ddr_by_day_df = ddr_by_day_df.append({'endDate':  date, 'number_of_flights': number_of_flights,
                                          'arrival_delayed_15_min_flights_number': arrival_delayed_15_min,
                                          'enroute_delayed_15_min_flights_number': enroute_delayed_15_min,
                                          'total_departure_delay': ddr_total_departure_delay,
                                          'average_departure_delay': ddr_average_departure_delay,
                                          'total_arrival_delay': ddr_total_arrival_delay,
                                          'average_arrival_delay': ddr_average_arrival_delay,
                                          'total_enroute_delay': ddr_total_enroute_delay,
                                          'average_enroute_delay': ddr_average_enroute_delay,
                                          'total_add_time_TMA': ddr_total_add_times,
                                          'average_add_time_TMA': ddr_average_add_time}, ignore_index=True)
    
    
filename = "ddr_stat_by_day_" + year + ".csv"

ddr_by_day_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.6f', header=None)

print("--- %s seconds ---" % ((time.time() - start_time)))