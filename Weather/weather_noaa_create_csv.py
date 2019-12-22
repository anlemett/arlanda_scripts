import pandas as pd
import numpy as np
from datetime import datetime
from calendar import monthrange
import pygrib # import pygrib interface to grib_api

year = "2018"
month = "04"

(first_day_weekday, number_of_days) = monthrange(int(year), int(month))

year_month = year[2:] + month
filename = 'gfsanl_3_' + year_month

NOAA_CSV = "noaa_" + year + '_' + month + ".csv"


print("before pygrib open")
grbs = pygrib.open(filename + '.grb2')
print("after pygrib open")

grib_df = pd.DataFrame(columns=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype=str)

for d in range(1,number_of_days+1):
    print(d)

    grb = grbs.select(name='Visibility', day=d, hour=12, minute=0, second=0)[0]
    visibilities = grb.values

    grb = grbs.select(name='Convective available potential energy', day=d, hour=12, minute=0, second=0)[0]
    capes = grb.values

    grb = grbs.select(name='Wind speed (gust)', day=d, hour=12, minute=0, second=0)[0]
    gusts = grb.values


    # lon: 16..19, lat: 58..61
    lat = 58
    for i in range(0,4):
        lon = 16
        for j in range(0,4):

            print(grb.dataDate)
            date = str(int(grb.dataDate))[2:]

            grib_df = grib_df.append({'date': date, 'lat': lat, 'lon': lon, 'visibility': visibilities[i][j],
                              'cape': capes[i][j], 'gust': gusts[i][j]}, ignore_index=True)
            lon = lon + 1
        lat = lat + 1

grib_df.to_csv(NOAA_CSV, sep=' ', encoding='utf-8', header=None, index=False)
