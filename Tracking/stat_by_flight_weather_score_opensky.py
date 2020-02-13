import pandas as pd


# flight_id date hour number_of_levels time_on_levels time_on_levels_percent distance_on_levels distance_on_levels_percent
opensky_stat_by_flight_df = pd.read_csv("data/statistics_opensky_2018/statistics_opensky_by_flight_2018.csv", sep=' ', index_col=0)


metrics_by_hour_df = pd.read_csv("data/weather/copernicus_year_metrics_kpis_2018.csv", sep=' ', index_col=0)
metrics_by_hour_df = metrics_by_hour_df[['date', 'hour', 'weather_score']]
metrics_by_hour_df.set_index(['date', 'hour'], inplace=True)




opensky_kpis_metrics_df = pd.DataFrame(columns=['flight_id', 'date', 'time_on_levels', 'weather_score'])


total_number_of_flights = len(opensky_stat_by_flight_df.groupby(level='flight_id'))
count = 0

for flight_id, flight_id_group in opensky_stat_by_flight_df.groupby(level='flight_id'):
    
    count = count +1    
    print(total_number_of_flights, count)
    
    date = flight_id_group.loc[flight_id]['date']    # 180101 - 181231
    hour = flight_id_group.loc[flight_id]['hour']
    
    time_on_levels = flight_id_group.loc[flight_id]['time_on_levels']
    
    weather_score = metrics_by_hour_df.loc[(date,hour)]['weather_score']
    
   
    opensky_kpis_metrics_df = opensky_kpis_metrics_df.append({'flight_id': flight_id, 'date': date, 'time_on_levels': time_on_levels,
                                                              'weather_score': weather_score
                                                             }, ignore_index=True)


opensky_kpis_metrics_df = opensky_kpis_metrics_df.astype({'flight_id': int})

opensky_kpis_metrics_df.to_csv("data/statistics_2018/statistics_opensky_by_flight_weather_score_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')
