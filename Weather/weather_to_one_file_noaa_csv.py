import pandas as pd
import os

year = '2018'
DATA_DIR = os.path.join("data", "weather_grib_csv_" + year)

filename = "grib_201801.csv"
df1 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201802.csv"
df2 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201803.csv"
df3 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201804.csv"
df4 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201805.csv"
df5 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201806.csv"
df6 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201807.csv"
df7 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201808.csv"
df8 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201809.csv"
df9 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201810.csv"
df10 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201811.csv"
df11 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})
filename = "grib_201812.csv"
df12 = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ', names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})

frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]

grib_df = pd.concat(frames)

grib_df = grib_df[(grib_df.lat==60) & (grib_df.lon==18)]
grib_df.reset_index(drop=True, inplace=True)

filename = "grib_2018.csv"
grib_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.6f', header=None)
