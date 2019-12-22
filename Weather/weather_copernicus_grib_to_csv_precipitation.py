import numpy as np
import pygrib # import pygrib interface to grib_api

import pandas as pd

grbs = pygrib.open('copernicus_TMA_cape_2018.grib')

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

for i in range(0,24):
    cape_all=np.array(grbs.select(name='Convective available potential energy', hour=i, minute=0, second=0))[0]

    cape=cape_all.data(lat1=my_y1,lat2=my_y2,lon1=my_x1,lon2=my_x2)
    #print(cape)
    for lat in range(8,-1,-1):
        for lon in range (8,-1,-1):
            new_d = {}
            new_d['time'] = i
            new_d['lat'] = cape[1][lat][0]
            new_d['lon'] = cape[2][0][lon]
            new_d['cape'] = cape[0][lat][lon]
            
            new_data.append(new_d)
            #print(i, cape[1][lat][0], cape[2][0][lon], cape[0][lat][lon])

data_df = pd.DataFrame(new_data, columns = ['time', 'lat', 'lon', 'cape'])

data_df.to_csv("copernicus_TMA_cape_2018.csv", sep=' ', encoding='utf-8', float_format='%.6f', header=True, index=False)
