import pandas as pd


ddr_stat_df = pd.read_csv("data/statistics_ddr_2018/statistics_ddr_by_hour_norm_2018.csv", sep=' ', index_col=0)

opensky_stat_df = pd.read_csv("data/statistics_opensky_2018/statistics_opensky_by_hour_norm_2018.csv", sep=' ')

year_ddr_stat_df = ddr_stat_df.loc[:, ('arrival_delay_mean', 'enroute_delay_mean', 'add_time_TMA_mean',
                                       'arrival_delay_median', 'enroute_delay_median', 'add_time_TMA_median',
                                       'number_of_flights')]
year_ddr_stat_df.rename(columns={'number_of_flights': 'ddr_number_of_flights'}, inplace=True)

year_opensky_stat_df = opensky_stat_df.loc[:, ('date', 'hour', 'average_time_on_levels', 'number_of_flights')]
year_opensky_stat_df.rename(columns={'number_of_flights': 'opensky_number_of_flights'}, inplace=True)


year_snow_df = pd.read_csv("data/weather/copernicus_TMA_snow_norm_2018.csv", sep=' ', index_col=0)
year_cape_df = pd.read_csv("data/weather/copernicus_TMA_cape_norm_2018.csv", sep=' ', index_col=0)
year_wind_df = pd.read_csv("data/weather/copernicus_TMA_wind_norm_2018.csv", sep=' ', index_col=0)
year_cloud_df = pd.read_csv("data/weather/copernicus_TMA_cloud_norm_2018.csv", sep=' ', index_col=0)


#year_metrics_kpis_df = pd.concat([year_ddr_stat_df, year_opensky_stat_df], axis=1)

year_metrics_kpis_df = pd.concat([year_ddr_stat_df, year_opensky_stat_df, 
                                  year_snow_df, year_cape_df, year_wind_df, year_cloud_df], axis=1)

year_metrics_kpis_df.to_csv("copernicus_ml_kpis_metrics_by_hour_2018.csv", sep=' ', encoding='utf-8')

print(year_metrics_kpis_df.head())


def getWeatherScore(sum):

    # sum: 0-5
    
    return int(sum/0.2)


year_metrics_kpis_df['flights_rsn_cape_i10fg_tcc'] = year_metrics_kpis_df.apply(lambda row: row['ddr_number_of_flights'] + row['rsn'] + row['cape'] + row['i10fg'] + row['tcc'], axis=1)
year_metrics_kpis_df['flights_rsn_cape_wind_tcc'] = year_metrics_kpis_df.apply(lambda row: row['ddr_number_of_flights'] + row['rsn'] + row['cape'] + row['wind'] + row['tcc'], axis=1)
year_metrics_kpis_df['flights_rsn_cape_wind'] = year_metrics_kpis_df.apply(lambda row: row['ddr_number_of_flights'] + row['rsn'] + row['cape'] + row['wind'], axis=1)

year_metrics_kpis_df['weather_score'] = year_metrics_kpis_df.apply(lambda row: getWeatherScore(row['flights_rsn_cape_i10fg_tcc']), axis=1)
year_metrics_kpis_df['weather_score2'] = year_metrics_kpis_df.apply(lambda row: getWeatherScore(row['flights_rsn_cape_wind_tcc']), axis=1)
year_metrics_kpis_df['weather_3metrics_score'] = year_metrics_kpis_df.apply(lambda row: getWeatherScore(row['flights_rsn_cape_wind']), axis=1)


year_metrics_kpis_df.to_csv("data/weather/copernicus_year_metrics_kpis_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')