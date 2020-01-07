import numpy as np
import pygrib # import pygrib interface to grib_api

import pandas as pd

year = 2018

grbs = pygrib.open('data/weather_copernicus_TMA_grib_2018/copernicus_TMA_precipitation_010118.grib')

#with open("copernicus_TMA_precipitation_2018.txt", "w") as text_file:
#    for grb in grbs:
#        print("{} {} {} {} {}#\n".format(grb.typeOfLevel,grb.level,grb.name,grb.shortName,grb.parameterUnits), file=text_file)
#    print("{}\n".format(grb.keys()), file=text_file)

#grbs.rewind() # rewind the iterator

my_y1 = 59
my_y2 = 61
my_x1 = 17
my_x2 = 19


new_data = []

import time

start_time = time.time()
     
selected_grbs=np.array(grbs.select(month=1, day=1))
for grb in selected_grbs:
    print(grb)
print("******************")

# No data for all hours

"""
for h in range(0,24):
            
            #selected_grbs=np.array(grbs.select(name='Total precipitation', month=m, day=d, hour=h, minute=0, second=0))
            #selected_grbs=np.array(grbs.select(name='Precipitation type', month=m, day=d, hour=h, minute=0, second=0))

            precipitation=selected_grbs[0].data(lat1=my_y1,lat2=my_y2,lon1=my_x1,lon2=my_x2)
            #print(precipitation)
            for lat_idx in range(8,-1,-1):
                for lon_idx in range (8,-1,-1):
                    new_d = {}
                    new_d['time'] = h
                    new_d['lat'] = precipitation[1][lat_idx][0]
                    new_d['lon'] = precipitation[2][0][lon_idx]
                    new_d['precipitation'] = precipitation[0][lat_idx][lon_idx]
            
                    new_data.append(new_d)

data_df = pd.DataFrame(new_data, columns = ['time', 'lat', 'lon', 'precipitation'])

data_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_precipitation_010118.csv", sep=' ', encoding='utf-8', float_format='%.6f', header=True, index=False)
"""
print((time.time()-start_time)/60)
