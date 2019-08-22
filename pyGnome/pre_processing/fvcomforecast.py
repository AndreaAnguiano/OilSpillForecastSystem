from netCDF4 import Dataset
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cutcoords import cutCoords
import os
import time

def fvcomforecast(startDate, endDate, path,prefix,sufix,latbox,lonbox, depths, uvar,vvar, latvar,lonvar, depthvar, path2save):
    dayofyr = startDate.timetuple().tm_yday
    daysd = startDate.day
    monthsd = startDate.month
    yearsd = startDate.year
    dayfd = endDate.day
    monthfd = endDate.month
    yearfd = endDate.year
    dayofyrf = endDate.timetuple().tm_yday
    yeardt = yearfd - yearsd
    firstFileName = 'Sargazo04_0001_sup.nc'
    #to do: first File name according to file's format 
    netcdfsname = [firstFileName] 
    #to do: netcdfsname according to how much files are
    
    data = Dataset(path + netcdfsname[0], 'r', format='NETCDF4_CLASSIC')
    var = data.variables
    u = var.get(uvar)
    v = var.get(vvar)
    latValues = var.get(latvar)
    lonValues = var.get(lonvar)
    timenetcdf = var.get('time')
    nvData = var.get('nv')
    fileName = 'fvcom_forecast_test.nc'
    #to do: rename fileName 
    dataset = Dataset(path2save+fileName, 'w', format='NETCDF3_CLASSIC')
    
    uData = u[:,0,:]
    vData = v[:,0,:]
    fillValue = 1.267651e+30

    # adding dimensions
    dataset.createDimension('time', None)
    dataset.createDimension('node', 14254)
    dataset.createDimension('nele', 26862)
    dataset.createDimension('three', 3)
    #to do: lack of dimensions (nbnd, nbi) 


    # Adding variables
    time = dataset.createVariable('time', np.float64, ('time',))
    lon = dataset.createVariable('lon', np.float32, ('node',))
    lat = dataset.createVariable('lat', np.float32, ('node',))
    u = dataset.createVariable('u', np.float32, ('time','nele',), fill_value=fillValue)
    v = dataset.createVariable('v', np.float32, ('time','nele',), fill_value=fillValue)
    nv = dataset.createVariable('nv', np.int32, ('three', 'nele',))
    
    #to do: lack of variables (bnb y nbe)
    # adding global atributtes
    dataset.grid_type = 'Triangular'

    # adding variables atributtes
    lat.long_name = 'nodal latitude'
    lat.units = 'degrees_north'
    lat.standard_name = 'latitude'

    lon.long_name = 'nodal longitude'
    lon.units = 'degrees_east'
    lon.standard_name = 'longitude'

    time.long_name = 'Time'
    time.units = 'days since 1858-11-17 00:00:00'
    time.standard_name = 'time'

    u.long_name = 'Eastward Water Velocity'
    u.standard_name = 'eastward_sea_water_velocity'
    u.units = 'm/s'

    v.long_name = 'Northward Water Velocity'
    v.standard_name = 'northward_sea_water_velocity'
    v.units = 'm/s'


    lat[:] = latValues[:]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]

    u[:] = uData[:]
    v[:] = vData[:]
    nv[:] = nvData[:]
    dataset.sync()
    dataset.close()





startdate = datetime(2019,8,19)
enddate = datetime(2019,8,19)
pth = '/DATA/forecastData/fvcom/'
pref = 'Sargazo04_'
latbox = [16, 17]
lonbox = [274, 272]
suf= '_sup.nc'
depths= [0]
latvar = 'lat'
lonvar = 'lon'
uvar = 'u'
vvar = 'v'
path2save = '/home/andrea/python/OilSpillForecastSystem/pyGnome/pre_processing/'
fileName = pth+pref+'0001'+suf
depthvar = 'siglay'
#model = 'fvcom'
fvcomforecast(startdate,enddate,pth,pref,suf,latbox,lonbox,depths, uvar,vvar, latvar, lonvar, depthvar,path2save)
