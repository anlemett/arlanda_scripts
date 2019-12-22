import pandas as pd
import numpy as np
from datetime import datetime
import pygrib # import pygrib interface to grib_api

year_month = "201802"

filename = 'gfsanl_3_' + year_month

GRIB_CSV = "grib_" + year_month + ".csv"


print("before pygrib open")
grbs = pygrib.open(filename + '.grb2')
print("after pygrib open")

grb = grbs.select()[0]
print(grb['latitudeOfFirstGridPointInDegrees'])
print(grb['latitudeOfLastGridPointInDegrees'])
print(grb['longitudeOfFirstGridPointInDegrees'])
print(grb['longitudeOfLastGridPointInDegrees'])

dat, lat, lon = grb.data()

print(lat)
print(lon)
