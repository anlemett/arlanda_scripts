import numpy as np
import pygrib # import pygrib interface to grib_api

import pandas as pd

grbs = pygrib.open('data/weather_copernicus_TMA_grib_2018/copernicus_TMA_cape_290718.grib')

#with open("data/weather_copernicus_TMA_csv_2018/copernicus_cape_290718.txt", "w") as text_file:
#    for grb in grbs:
#        print("{} {} {} {} {}\n".format(grb.typeOfLevel,grb.level,grb.name,grb.shortName,grb.parameterUnits), file=text_file)
#    print("{}\n".format(grb.keys()), file=text_file)

#grbs.rewind() # rewind the iterator

my_y1 = 59
my_y2 = 61
my_x1 = 17
my_x2 = 19


new_data = []

for i in range(0,24):
    selected_grbs=np.array(grbs.select(name='Convective available potential energy', hour=i, minute=0, second=0))

    cape=selected_grbs[0].data(lat1=my_y1,lat2=my_y2,lon1=my_x1,lon2=my_x2)
    #print(cape)
    for lat_idx in range(8,-1,-1):
        for lon_idx in range (8,-1,-1):
            new_d = {}
            new_d['time'] = i
            new_d['lat'] = cape[1][lat_idx][0]
            new_d['lon'] = cape[2][0][lon_idx]
            new_d['cape'] = cape[0][lat_idx][lon_idx]
            
            new_data.append(new_d)


data_df = pd.DataFrame(new_data, columns = ['time', 'lat', 'lon', 'cape'])

data_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cape_290718.csv", sep=' ', encoding='utf-8', float_format='%.6f', header=True, index=False)
