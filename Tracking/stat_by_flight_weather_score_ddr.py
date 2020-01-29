import pandas as pd


# end_date end_time end_hour flight_id departure_delay arrival_delay enroute_delay add_time
ddr_stat_by_flight_df = pd.read_csv("data/statistics_ddr_2018/statistics_ddr_by_flight_2018.csv", sep=' ', index_col=0,
                                    dtype={'flight_id':int})
ddr_stat_by_flight_df.set_index('flight_id', inplace = True)


metrics_by_hour_df = pd.read_csv("data/weather/copernicus_year_metrics_kpis_2018.csv", sep=' ', index_col=0)
metrics_by_hour_df = metrics_by_hour_df[['date', 'hour', 'weather_score']]
metrics_by_hour_df.set_index(['date', 'hour'], inplace=True)



ddr_kpis_metrics_df = pd.DataFrame(columns=['flight_id', 'date', 'add_time', 'weather_score'])


total_number_of_flights = len(ddr_stat_by_flight_df.groupby(level='flight_id'))
count = 0

for flight_id, flight_id_group in ddr_stat_by_flight_df.groupby(level='flight_id'):
    
    count = count +1    
    print(total_number_of_flights, count)
    
    date = flight_id_group.loc[flight_id]['end_date']    # 180101 - 181231
    hour = flight_id_group.loc[flight_id]['end_hour']
    
    add_time = flight_id_group.loc[flight_id]['add_time']
    
    weather_score = metrics_by_hour_df.loc[(date,hour)]['weather_score']
    
   
    ddr_kpis_metrics_df = ddr_kpis_metrics_df.append({'flight_id': flight_id, 'date': date, 'add_time': add_time,
                                                      'weather_score': weather_score
                                                     }, ignore_index=True)


ddr_kpis_metrics_df = ddr_kpis_metrics_df.astype({'flight_id': int})

ddr_kpis_metrics_df.to_csv("data/statistics_2018/statistics_ddr_by_flight_weather_score_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')
