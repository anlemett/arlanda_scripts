import pandas as pd
import numpy as np
from datetime import datetime
import pygrib # import pygrib interface to grib_api

filename = 'T+06_0600'


print("before pygrib open")
#grbs = pygrib.open(filename + '.grb2')
grbs = pygrib.open(filename)
print("after pygrib open")


with open(filename + "_parameters.txt", "w") as text_file:
    for grb in grbs:
        #print("{}\n".format(grb), file=text_file)
        print("{} {} {} {} {}\n".format(grb.typeOfLevel,grb.level,grb.name,grb.shortName,grb.parameterUnits), file=text_file)
    print("{}\n".format(grb.keys()), file=text_file)

grb = grbs.select()[0]
print(grb['latitudeOfFirstGridPointInDegrees'])
print(grb['latitudeOfLastGridPointInDegrees'])
print(grb['longitudeOfFirstGridPointInDegrees'])
print(grb['longitudeOfLastGridPointInDegrees'])

print(grb)
print("grb printed")


grb = grbs.select(name='Relative humidity')[0]
humidity = grb.values

print(humidity)
#a = grb.values
#dat, lat, lon = grb.data()
#print(lat)
#print(lon)
