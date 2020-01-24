import pandas as pd


# end_date end_time end_hour flight_id departure_delay arrival_delay enroute_delay add_time
ddr_stat_by_flight_df = pd.read_csv("data/statistics_ddr_2018/statistics_ddr_by_flight_2018.csv", sep=' ', index_col=0,
                                    dtype={'flight_id':int})
ddr_stat_by_flight_df.set_index('flight_id', inplace = True)
# flight_id date hour number_of_levels time_on_levels time_on_levels_percent distance_on_levels distance_on_levels_percent
opensky_stat_by_flight_df = pd.read_csv("data/statistics_opensky_2018/statistics_opensky_by_flight_2018.csv", sep=' ', index_col=0)


#  end_date end_hour number_of_flights arrival_delayed_15_min_flights_number enroute_delayed_15_min_flights_number total_departure_delay
#  average_departure_delay total_arrival_delay average_arrival_delay total_enroute_delay average_enroute_delay total_add_time_TMA
# average_add_time_TMA min_add_time_TMA max_add_time_TMA
ddr_stat_by_hour_df = pd.read_csv("data/statistics_ddr_2018/statistics_ddr_by_hour_norm_2018.csv", sep=' ', index_col=0)


snow_df = pd.read_csv("data/weather/copernicus_TMA_snow_mean_2018.csv", sep=' ', index_col=0)
cape_df = pd.read_csv("data/weather/copernicus_TMA_cape_mean_2018.csv", sep=' ', index_col=0)
wind_df = pd.read_csv("data/weather/copernicus_TMA_wind_mean_2018.csv", sep=' ', index_col=0)
cloud_df = pd.read_csv("data/weather/copernicus_TMA_cloud_mean_2018.csv", sep=' ', index_col=0)
add_weather_df = pd.read_csv("data/weather/copernicus_TMA_add_weather_mean_2018.csv", sep=' ', index_col=0)


metrics_by_hour_df = pd.concat([ddr_stat_by_hour_df, snow_df, cape_df, wind_df, cloud_df, add_weather_df], axis=1)

metrics_by_hour_df = metrics_by_hour_df[['date', 'hour', 'number_of_flights', 'sd', 'rsn', 'cape', 'i10fg', 'wind', 't2m', 'hcc', 'lcc', 'mcc']]
                                         #'crr', 'csf', 'csdr', 'mcpr', 'msr', 'mtpr']]


metrics_by_hour_df.set_index(['date', 'hour'], inplace=True)




ddr_kpis_metrics_df = pd.DataFrame(columns=['flight_id', 'add_time',
                                            'number_of_flights',
                                            'sd', 'rsn', 'cape', 'i10fg', 'wind', 't2m', 'hcc', 'lcc', 'mcc'
                                            ])


total_number_of_flights = len(ddr_stat_by_flight_df.groupby(level='flight_id'))
count = 0

for flight_id, flight_id_group in ddr_stat_by_flight_df.groupby(level='flight_id'):
    
    count = count +1    
    print(total_number_of_flights, count)
    
    date = flight_id_group.loc[flight_id]['end_date']    # 180101 - 181231
    hour = flight_id_group.loc[flight_id]['end_hour']
    
    add_time = flight_id_group.loc[flight_id]['add_time']
    
    number_of_flights = metrics_by_hour_df.loc[(date,hour)]['number_of_flights']
    sd = metrics_by_hour_df.loc[(date,hour)]['sd']
    rsn = metrics_by_hour_df.loc[(date,hour)]['rsn']
    cape = metrics_by_hour_df.loc[(date,hour)]['cape']
    i10fg = metrics_by_hour_df.loc[(date,hour)]['i10fg']
    wind = metrics_by_hour_df.loc[(date,hour)]['wind']
    t2m = metrics_by_hour_df.loc[(date,hour)]['t2m']
    hcc = metrics_by_hour_df.loc[(date,hour)]['hcc']
    lcc = metrics_by_hour_df.loc[(date,hour)]['lcc']
    mcc = metrics_by_hour_df.loc[(date,hour)]['mcc']
    
   
    ddr_kpis_metrics_df = ddr_kpis_metrics_df.append({'flight_id': flight_id, 'add_time': add_time, 'number_of_flights': number_of_flights,
                                                      'sd': sd, 'rsn': rsn, 'cape': cape, 'i10fg': i10fg, 'wind': wind, 't2m': t2m, 
                                                      'hcc': hcc, 'lcc': lcc, 'mcc': mcc
                                                     }, ignore_index=True)


ddr_kpis_metrics_df = ddr_kpis_metrics_df.astype({'flight_id': int})

ddr_kpis_metrics_df.to_csv("data/statistics_2018/statistics_ddr_by_flight_kpis_metrics_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')
