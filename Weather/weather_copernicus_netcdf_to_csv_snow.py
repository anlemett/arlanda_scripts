import xarray as xr

year = 2018


def getMonth(pandas_timestamp):
    return pandas_timestamp.to_pydatetime().month

def getDay(pandas_timestamp):
    return pandas_timestamp.to_pydatetime().day

def getHour(pandas_timestamp):
    return pandas_timestamp.to_pydatetime().hour


import time
start_time = time.time()


nc_filename = 'data/weather_copernicus_TMA_grib_2018/copernicus_TMA_snow_2018.nc'
DS = xr.open_dataset(nc_filename)

df = DS.to_dataframe()

df.reset_index(inplace=True)

print(df.head())



df['month'] = df.apply(lambda row: getMonth(row['time']), axis=1)

df['day'] = df.apply(lambda row: getDay(row['time']), axis=1)

df['hour'] = df.apply(lambda row: getHour(row['time']), axis=1)



df = df[['month','day','hour', 'lat', 'lon', 'rsn', 'sd']] # rsn - snow density, sd - snow depth

df = df.sort_values(by = ['month', 'day', 'hour', 'lat', 'lon'], ascending = [True, True, True, True, False])

df.to_csv('data/weather_copernicus_TMA_csv_2018/copernicus_TMA_snow_2018.csv', sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

print((time.time()-start_time)/60)