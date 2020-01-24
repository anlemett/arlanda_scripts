import xarray as xr
from math import sqrt

year = 2018


def getMonth(pandas_timestamp):
    return pandas_timestamp.to_pydatetime().month

def getDay(pandas_timestamp):
    return pandas_timestamp.to_pydatetime().day

def getHour(pandas_timestamp):
    return pandas_timestamp.to_pydatetime().hour

def getWind(u, v):

    return sqrt(u**2+v**2)


import time
start_time = time.time()


nc_filename = 'data/weather_copernicus_TMA_grib_2018/copernicus_TMA_add_weather_2018.nc'
DS = xr.open_dataset(nc_filename)

df = DS.to_dataframe()

df.reset_index(inplace=True)

print(df.head())


df['month'] = df.apply(lambda row: getMonth(row['time']), axis=1)

df['day'] = df.apply(lambda row: getDay(row['time']), axis=1)

df['hour'] = df.apply(lambda row: getHour(row['time']), axis=1)




df = df[['month','day','hour', 'latitude', 'longitude', 't2m', 'crr', 'csf', 'csfr', 'hcc', 'lcc', 'mcpr', 'msr', 'mtpr', 'mcc']]
# t2m - 2 metre temperature
# cp - Convective precipitation
# crr - Convective rain rate
# csf - Convective snowfall
# csfr - Convective snowfall rate water equivalent
# hcc - High cloud cover
# lcc - Low cloud cover
# mcpr - Mean convective precipitation rate
# msr - Mean snowfall rate
# mtpr - Mean total precipitation rate
# mcc - Medium cloud cover

df.rename(columns={'latitude': 'lat', 'longitude': 'lon'}, inplace=True)

df = df.sort_values(by = ['month', 'day', 'hour', 'lat', 'lon'], ascending = [True, True, True, True, False])

df.to_csv('data/weather_copernicus_TMA_csv_2018/copernicus_TMA_add_weather_2018.csv', sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

print((time.time()-start_time)/60)