import pandas as pd
import numpy as np

import cfgrib


filename = 'T+06_0600'

#Filt = {'typeOfLevel': 'maxWind'}
Filt = {'typeOfLevel': 'isobaricInhPa'}
#Filt = {'typeOfLevel': 'tropopause'}
#Filt = {'typeOfLevel': 'isobaricInhPa', 'shortName': 'r'}
#Filt = {'typeOfLevel': 'isobaricInhPa', 'name': 'Relative humidity'}


#ds = cfgrib.open_file(filename,filter_by_keys=Filt)
#ds = cfgrib.open_file(filename)

import xarray as xr
ds = xr.open_dataset(filename, engine="cfgrib", backend_kwargs={'filter_by_keys': Filt})

print(ds)
#check out the data:
#print(ds.dimensions.keys())
#print(ds.variables.keys())

#retrieve the dimension values:
timeLevel = ds.variables['time'].data
longitude = ds.variables['latitude'].data
latitude = ds.variables['longitude'].data

#Query gridpoint at specific time, latitude and longitude indices:
iTime = 0
iLat= 60
iLon = 170
#ds.variables['r'].data[:,iTime,iLat,iLon].mean()
print(ds.variables['r'].data[4,iLat,iLon])