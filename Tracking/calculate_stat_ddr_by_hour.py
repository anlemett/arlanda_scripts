import pandas as pd
import numpy as np
import os

import time
start_time = time.time()

year = '2018'

DATA_DIR = os.path.join("data", "statistics_ddr_" + year)


filename = "statistics_ddr_by_flight_" + year + ".csv"

# endDate endTime endHour flightId departure_delay arrival_delay enroute_delay add_TMA_Time
ddr_by_flight_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
                               dtype={'endDate':str, 'endTime':str, 'endHour':int, 'flightId':int, 
                                      'departure_delay':int, 'arrival_delay':int,
                                      'enroute_delay':int, 'add_TMA_time':int
                                      })

ddr_by_flight_df.set_index(['endDate'], inplace=True)

ddr_by_hour_df = pd.DataFrame(columns=['end_date', 'end_hour', 'number_of_flights',
                                      'arrival_delayed_15_min_flights_number',
                                      'enroute_delayed_15_min_flights_number',
                                      'departure_delay_total', 'departure_delay_mean', 'departure_delay_median',                                      
                                      'arrival_delay_total', 'arrival_delay_mean', 'arrival_delay_median',
                                      'enroute_delay_total', 'enroute_delay_mean', 'enroute_delay_median',
                                      'add_time_TMA_total', 'add_time_TMA_mean', 'add_time_TMA_median',                               
                                      'add_time_TMA_min', 'add_time_TMA_max'])

days_num = len(ddr_by_flight_df.groupby(level='endDate'))
print(days_num)


for date, date_df in ddr_by_flight_df.groupby(level='endDate'):
    
    print(date)
    
    for hour in range(0,24):
        
        hour_df = date_df[date_df['endHour'] == hour]
    
        number_of_flights = len(hour_df)
        
        if number_of_flights ==0:
            arrival_delayed_15_min = 0
            enroute_delayed_15_min = 0
            ddr_total_departure_delay = 0
            ddr_average_departure_delay = 0
            ddr_total_arrival_delay = 0
            ddr_average_arrival_delay = 0
            ddr_total_enroute_delay = 0
            ddr_average_enroute_delay = 0
            ddr_total_add_time = 0
            ddr_average_add_time = 0
            ddr_min_add_time = 0
            ddr_max_add_time = 0
            
        else:            
    
            arrival_delayed_15_min_df = hour_df.loc[hour_df.arrival_delay > 900, 'arrival_delay']
            arrival_delayed_15_min = len (arrival_delayed_15_min_df)

            enroute_delayed_15_min_df = hour_df.loc[hour_df.enroute_delay > 900, 'enroute_delay']
            enroute_delayed_15_min = len (enroute_delayed_15_min_df)

            departure_delays = hour_df.loc[hour_df.departure_delay > 0, 'departure_delay']
            ddr_total_departure_delay = int(np.sum(departure_delays)) if departure_delays.any() else 0
            ddr_average_departure_delay = int(ddr_total_departure_delay/number_of_flights) if departure_delays.any() else 0
            ddr_median_departure_delay = int(np.median(departure_delays)) if departure_delays.any() else 0

            arrival_delays = hour_df.loc[hour_df.arrival_delay > 0, 'arrival_delay']
            ddr_total_arrival_delay = int(np.sum(arrival_delays)) if arrival_delays.any() else 0
            ddr_average_arrival_delay = int(ddr_total_arrival_delay/number_of_flights) if arrival_delays.any() else 0
            ddr_median_arrival_delay = int(np.median(arrival_delays)) if arrival_delays.any() else 0

            enroute_delays = hour_df.loc[hour_df.enroute_delay > 0, 'enroute_delay']
            ddr_total_enroute_delay = int(np.sum(enroute_delays)) if enroute_delays.any() else 0
            ddr_average_enroute_delay = int(ddr_total_enroute_delay/number_of_flights) if enroute_delays.any() else 0
            ddr_median_enroute_delay = int(np.median(enroute_delays)) if enroute_delays.any() else 0

            add_times = hour_df[['add_TMA_time']]
            ddr_min_add_time = int(np.min(add_times))
            ddr_max_add_time = int(np.max(add_times))
            
            add_times = hour_df.loc[hour_df.add_TMA_time > 0, 'add_TMA_time']
            ddr_total_add_time = int(np.sum(add_times)) if add_times.any() else 0
            ddr_average_add_time = int(ddr_total_add_time/number_of_flights) if add_times.any() else 0
            ddr_median_add_time = int(np.median(add_times)) if add_times.any() else 0




        ddr_by_hour_df = ddr_by_hour_df.append({'end_date':  date, 'end_hour': hour,
                                          'number_of_flights': number_of_flights,
                                          'arrival_delayed_15_min_flights_number': arrival_delayed_15_min,
                                          'enroute_delayed_15_min_flights_number': enroute_delayed_15_min,
                                          'departure_delay_total': ddr_total_departure_delay,
                                          'departure_delay_mean': ddr_average_departure_delay,
                                          'departure_delay_median': ddr_median_departure_delay,
                                          'arrival_delay_total': ddr_total_arrival_delay,
                                          'arrival_delay_mean': ddr_average_arrival_delay,
                                          'arrival_delay_median': ddr_median_arrival_delay,
                                          'enroute_delay_total': ddr_total_enroute_delay,
                                          'enroute_delay_mean': ddr_average_enroute_delay,
                                          'enroute_delay_median': ddr_median_enroute_delay,
                                          'add_time_TMA_total': ddr_total_add_time,
                                          'add_time_TMA_mean': ddr_average_add_time,
                                          'add_time_TMA_median': ddr_median_add_time,
                                          'add_time_TMA_min': ddr_min_add_time, 'add_time_TMA_max': ddr_max_add_time
                                          }, ignore_index=True)
    
    
filename = "statistics_ddr_by_hour_" + year + ".csv"

#end_date end_hour number_of_flights arrival_delayed_15_min_flights_number enroute_delayed_15_min_flights_number total_departure_delay average_departure_delay total_arrival_delay average_arrival_delay total_enroute_delay average_enroute_delay total_add_time_TMA average_add_time_TMA min_add_time_TMA max_add_time_TMA
ddr_by_hour_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

print("--- %s seconds ---" % ((time.time() - start_time)))