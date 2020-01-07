import numpy as np
import pygrib # import pygrib interface to grib_api

import pandas as pd

year = 2018

grbs = pygrib.open('data/weather_copernicus_TMA_grib_2018/copernicus_TMA_wind_010118.grib')

#with open("copernicus_TMA_wind_2018.txt", "w") as text_file:
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


for h in range(0,24):
    # No data for all hours for wind gust
    #selected_grbs=np.array(grbs.select(name='Instantaneous 10 metre wind gust', month=1, day=1, hour=h, minute=0, second=0))
    #wind_gust = selected_grbs[0].data(lat1=my_y1,lat2=my_y2,lon1=my_x1,lon2=my_x2)
    
    selected_grbs=np.array(grbs.select(name='10 metre U wind component', month=1, day=1, hour=h, minute=0, second=0))
    u_component = selected_grbs[0].data(lat1=my_y1,lat2=my_y2,lon1=my_x1,lon2=my_x2)
    
    selected_grbs=np.array(grbs.select(name='10 metre V wind component', month=1, day=1, hour=h, minute=0, second=0))
    v_component = selected_grbs[0].data(lat1=my_y1,lat2=my_y2,lon1=my_x1,lon2=my_x2)

    

    for lat_idx in range(8,-1,-1):
        for lon_idx in range (8,-1,-1):
            new_d = {}
            new_d['time'] = h
            new_d['u_component'] = u_component[0][lat_idx][lon_idx]
            new_d['v_component'] = v_component[0][lat_idx][lon_idx]
            
            new_d['lat'] = u_component[1][lat_idx][0]
            new_d['lon'] = u_component[2][0][lon_idx]
            
            new_data.append(new_d)

#data_df = pd.DataFrame(new_data, columns = ['time', 'lat', 'lon', 'wind_gust', 'u_component', 'v_component'])
data_df = pd.DataFrame(new_data, columns = ['time', 'lat', 'lon', 'u_component', 'v_component'])

data_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_wind_010118.csv", sep=' ', encoding='utf-8', float_format='%.6f', header=True, index=False)

print((time.time()-start_time)/60)
