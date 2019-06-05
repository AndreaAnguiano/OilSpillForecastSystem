from netCDF4 import Dataset
from datetime import datetime
import numpy as np
import pandas as pd
import math as m
from cutcoords import cutCoords

def wrfforecast(startDate, endDate, path, prefix,sufix, latbox, lonbox, uvar, vvar, latvar, lonvar, path2save):
    dayofyr = startDate.timetuple().tm_yday
    daysd = startDate.day
    monthsd = startDate.month
    yearsd = startDate.year
    dayfd = endDate.day
    monthfd = endDate.month
    yearfd = endDate.year
    dayofyrf = endDate.timetuple().tm_yday
    yeardt = yearfd - yearsd
    fileName = path + prefix + str(yearsd) + "-" +"{0:02d}".format(monthsd)+'-'+ "{0:02d}".format(daysd)+sufix
    #print fileName
    coords = cutCoords(fileName, latvar, lonvar, latbox, lonbox, 'depth', 'depthvar', 'wrf')

    latValues = coords[0]
    lonValues = coords[1]
    latminindx = coords[2]
    latmaxindx = coords[3]
    lonminindx = coords[4]
    lonmaxindx = coords[5]
    # print 'latvalues: ',latValues.shape,'lonvalues: ', lonValues.shape  
    data = Dataset(fileName, 'r', format='NETCDF4_CLASSIC')
    var = data.variables
    u = var.get(uvar)
    v = var.get(vvar)
    ncTime = var.get('Times')
    uData = np.zeros((len(ncTime), len(latValues), len(lonValues)))
    vData = np.zeros((len(ncTime), len(latValues), len(lonValues)))
    #print 'udata: ', uData.shape, 'vdata: ', vData.shape
    for hour in range(0,len(ncTime)):
        uData[hour, :, :] = u[hour,latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
        vData[hour, :, :] = v[hour,latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
    
    fileName = 'WRF_forecast_' + str(yearsd) + "{0:02d}".format(monthsd) + "{0:02d}".format(daysd) +'.nc'
    dataset = Dataset(path2save + fileName, 'w', format='NETCDF3_CLASSIC')

    fillValue = 1.267651e+30

    # adding dimensions
    dataset.createDimension('time', None)
    dataset.createDimension('lat', len(latValues))
    dataset.createDimension('lon', len(lonValues))

    # Adding variables
    time = dataset.createVariable('time', np.float64, ('time',))
    lon = dataset.createVariable('lon', np.float32, ('lon',))
    lat = dataset.createVariable('lat', np.float32, ('lat',))
    u = dataset.createVariable('u', np.float32, ('time', 'lat', 'lon',), fill_value=fillValue)
    v = dataset.createVariable('v', np.float32, ('time','lat', 'lon',), fill_value=fillValue)

    # adding global atributtes
    dataset.grid_type = 'REGULAR'

    # adding variables atributtes
    lat.long_name = 'Latitude'
    lat.units = 'degrees_east'
    lat.standard_name = 'latitude'

    lon.long_name = 'Longitude'
    lon.units = 'degrees_north'
    lon.standard_name = 'longitude'

    time.long_name = 'Time'
    time.units = 'hours since ' + str(yearsd) + '-' + str(monthsd) + '-' + str(daysd) + ' 00:00:00'
    time.standard_name = 'time'

    u.long_name = 'Eastward Water Velocity'
    u.standard_name = 'eastward_sea_water_velocity'
    u.units = 'm/s'

    v.long_name = 'Northward Water Velocity'
    v.standard_name = 'northward_sea_water_velocity'
    v.units = 'm/s'

    timenetcdf = [x for x in range(1, len(ncTime) +1)]

    lat[:] = latValues[:]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]
    u[:] = uData[:]
    v[:] = vData[:]

    dataset.sync()
    dataset.close()



#startdate = datetime(2019,04,01)
#enddate = datetime(2019,04,01)
#pth = '/DATA/forecastData/wrf/04_abril/'
#pref = 'wrfout_d01_'
#dpth = [0]
#lat = [18.2, 31]
#lon = [-98, -83]
#suf= '_00.nc'
#latvar = 'XLAT'
#lonvar = 'XLONG'
#uvar = 'U10'
#vvar = 'V10'
#path2save = '../../Data/Winds/'
#import time

#tic = time.clock()

#wrfforecast(startdate, enddate, pth,pref, suf, lat, lon,uvar, vvar, latvar,lonvar, path2save)
#toc = time.clock()
#print(toc - tic)
