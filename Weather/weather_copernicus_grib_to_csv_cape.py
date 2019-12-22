import numpy as np
import pygrib # import pygrib interface to grib_api

import pandas as pd

grbs = pygrib.open('data/weather_copernicus_TMA_grib_2018/copernicus_TMA_cape_2018.grib')

#with open("copernicus_cape_2018.txt", "w") as text_file:
#    for grb in grbs:
#        print("{} {} {} {} {}#\n".format(grb.typeOfLevel,grb.level,grb.name,grb.shortName,grb.parameterUnits), file=text_file)
#    print("{}\n".format(grb.keys()), file=text_file)

#grbs.rewind() # rewind the iterator

my_y1 = 59
my_y2 = 61
my_x1 = 17
my_x2 = 19


new_data = []

for d in range(1,32):
    for h in range(0,24):
    	cape_all=np.array(grbs.select(name='Convective available potential energy', day=d, hour=h, minute=0, second=0))[0]
    	print(cape_all.year)
    	print(cape_all.month)
    	print(cape_all.day)
    	print(cape_all.hour)
    	cape=cape_all.data(lat1=my_y1,lat2=my_y2,lon1=my_x1,lon2=my_x2)
    	#print(cape)
    	for lat in range(8,-1,-1):
    	    for lon in range (8,-1,-1):
    	        new_d = {}
    	        new_d['time'] = h
    	        new_d['lat'] = cape[1][lat][0]
    	        new_d['lon'] = cape[2][0][lon]
    	        new_d['cape'] = cape[0][lat][lon]
            
    	        new_data.append(new_d)
    	        #print(i, cape[1][lat][0], cape[2][0][lon], cape[0][lat][lon])

data_df = pd.DataFrame(new_data, columns = ['time', 'lat', 'lon', 'cape'])

data_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cape_2018.csv", sep=' ', encoding='utf-8', float_format='%.6f', header=True, index=False)
