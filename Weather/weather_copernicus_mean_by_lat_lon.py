import pandas as pd

snow_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_snow_norm_2018.csv", sep=' ', index_col=0)
cape_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cape_norm_2018.csv", sep=' ', index_col=0)
wind_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_wind_norm_2018.csv", sep=' ', index_col=0)
cloud_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cloud_2018.csv", sep=' ', index_col=0)
add_weather_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_add_weather_norm_2018.csv", sep=' ', index_col=0)


cloud_df.set_index(['month', 'day', 'hour'], inplace=True)

mean_cloud = []
for idx, hour_df in cloud_df.groupby(level=[0, 1, 2]):
    mean_cloud.append(round(hour_df['tcc'].mean(),3))

year_cloud_df = pd.DataFrame()
year_cloud_df['tcc'] = mean_cloud
year_cloud_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cloud_mean_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')



snow_df.set_index(['month', 'day', 'hour'], inplace=True)

mean_snow_depth = []
mean_snow_density = []
for idx, hour_df in snow_df.groupby(level=[0, 1, 2]):
    mean_snow_depth.append(round(hour_df['sd'].mean(),3))
    mean_snow_density.append(round(hour_df['rsn'].mean(),3))
    
year_snow_df = pd.DataFrame()
year_snow_df['sd'] = mean_snow_depth
year_snow_df['rsn'] = mean_snow_density
year_snow_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_snow_mean_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')



cape_df.set_index(['month', 'day', 'hour'], inplace=True)

mean_cape = []
date = []
hour = []
for idx, hour_df in cape_df.groupby(level=[0, 1, 2]):
    mean_cape.append(round(hour_df['cape'].mean(),3))
    date.append(hour_df['date'][0])
    hour.append(idx[2])

year_cape_df = pd.DataFrame()
year_cape_df['cape'] = mean_cape
year_cape_df['date'] = date
year_cape_df['hour'] = hour
year_cape_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cape_mean_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')



wind_df.set_index(['month', 'day', 'hour'], inplace=True)

mean_wind_gust = []
mean_wind = []
for idx, hour_df in wind_df.groupby(level=[0, 1, 2]):
    mean_wind_gust.append(round(hour_df['i10fg'].mean(),3))
    mean_wind.append(round(hour_df['wind'].mean(),3))

year_wind_df = pd.DataFrame()
year_wind_df['i10fg'] = mean_wind_gust
year_wind_df['wind'] = mean_wind
year_wind_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_wind_mean_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')



add_weather_df.set_index(['month', 'day', 'hour'], inplace=True)
# 't2m', 'crr', 'csf', 'csfr', 'hcc', 'lcc', 'mcpr', 'msr', 'mtpr', 'mcc'
mean_t2m = []
mean_crr = []
mean_csf = []
mean_csfr = []
mean_hcc = []
mean_lcc = []
mean_mcpr = []
mean_msr = []
mean_mtpr = []
mean_mcc = []


for idx, hour_df in add_weather_df.groupby(level=[0, 1, 2]):
    mean_t2m.append(round(hour_df['t2m'].mean(),3))
    mean_crr.append(round(hour_df['crr'].mean(),3))
    mean_csf.append(round(hour_df['csf'].mean(),3))
    mean_csfr.append(round(hour_df['csfr'].mean(),3))
    mean_hcc.append(round(hour_df['hcc'].mean(),3))
    mean_lcc.append(round(hour_df['lcc'].mean(),3))
    mean_mcpr.append(round(hour_df['mcpr'].mean(),3))
    mean_msr.append(round(hour_df['msr'].mean(),3))
    mean_mtpr.append(round(hour_df['mtpr'].mean(),3))
    mean_mcc.append(round(hour_df['mcc'].mean(),3))
    
year_add_weather_df = pd.DataFrame()
year_add_weather_df['t2m'] = mean_t2m
year_add_weather_df['crr'] = mean_crr
year_add_weather_df['csf'] = mean_csf
year_add_weather_df['csdr'] = mean_csfr
year_add_weather_df['hcc'] = mean_hcc
year_add_weather_df['lcc'] = mean_lcc
year_add_weather_df['mcpr'] = mean_mcpr
year_add_weather_df['msr'] = mean_msr
year_add_weather_df['mtpr'] = mean_mtpr
year_add_weather_df['mcc'] = mean_mcc

year_add_weather_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_add_weather_mean_2018.csv", sep=' ', float_format='%.3f', encoding='utf-8')
