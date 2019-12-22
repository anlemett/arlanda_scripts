import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2018'

DATA_DIR = os.path.join("data", "statistics_opensky_" + year)

input_filename = "statistics_opensky_by_flight_" + year + ".csv"
output_filename = "statistics_opensky_by_day_" + year + ".csv"

#flight_id date number_of_levels time_on_levels time_on_levels_percent distance_on_levels distance_on_levels_percent
vfe_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'date': str})


vfe_df.set_index(['date'], inplace=True)

vfe_by_day_df = pd.DataFrame(columns=['date', 'number_of_flights', 'number_of_level_flights', 'total_number_of_levels', 'average_number_of_levels',
                            'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'])


for date, new_df in vfe_df.groupby(level='date'):

    number_of_flights = len(new_df)
    
    level_df = new_df[new_df['number_of_levels']>0]
    
    number_of_level_flights = len(level_df)
    
    number_of_levels_day = new_df['number_of_levels'].values # np array

    total_number_of_levels_day = np.sum(number_of_levels_day)

    average_number_of_levels_day = total_number_of_levels_day/len(number_of_levels_day) if number_of_levels_day.any() else 0

    time_on_levels_day = new_df['time_on_levels'].values # np array
    total_time_on_levels_day = np.sum(time_on_levels_day)
    average_time_on_levels_day = total_time_on_levels_day/len(time_on_levels_day) if time_on_levels_day.any() else 0

    distance_on_levels_day = new_df['distance_on_levels'].values # np array
    total_distance_on_levels_day = np.sum(distance_on_levels_day)
    average_distance_on_levels_day = total_distance_on_levels_day/len(distance_on_levels_day) if distance_on_levels_day.any() else 0

    vfe_by_day_df = vfe_by_day_df.append({'date': date, 'number_of_flights': number_of_flights, 'number_of_level_flights': number_of_level_flights,
    'total_number_of_levels': total_number_of_levels_day, 'average_number_of_levels': average_number_of_levels_day,
    'total_time_on_levels': total_time_on_levels_day, 'average_time_on_levels': average_time_on_levels_day,
    'total_distance_on_levels': total_distance_on_levels_day, 'average_distance_on_levels': average_distance_on_levels_day
    }, ignore_index=True)

# not all dates in opensky states, creating empty rows for missing dates
(nrows, ncol) = vfe_by_day_df.shape

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
month_date_list = []

for month in months:
    (first_day_weekday, number_of_days) = monthrange(int(year), int(month))
    
    date = "18" + month
        
    for d in range(1,9):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,number_of_days+1):
        month_date_list.append(date + str(d))
    df_dates_np = vfe_by_day_df.iloc[:,0].values
        
for d in month_date_list:
    if d not in df_dates_np:
        vfe_by_day_df = vfe_by_day_df.append({'date': d, 'number_of_flights': 0, 'number_of_level_flights':0,
                                              'total_number_of_levels': 0, 'average_number_of_levels': 0,
                                              'total_time_on_levels': 0, 'average_time_on_levels': 0,
                                              'total_distance_on_levels': 0, 'average_distance_on_levels': 0
                                              }, ignore_index=True)

vfe_by_day_df = vfe_by_day_df.sort_values(by ='date' )
vfe_by_day_df.reset_index(drop=True, inplace=True)


vfe_by_day_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.6f', header=None)

print("--- %s minutes ---" % ((time.time() - start_time)/60))