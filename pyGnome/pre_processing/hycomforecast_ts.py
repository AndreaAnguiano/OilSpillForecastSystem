from netCDF4 import Dataset
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cutcoords import cutCoords
import os
import time

def hycomforecast_ts(startDate, endDate, path,prefix,sufix,latbox,lonbox, depths, uvar,vvar, latvar,lonvar, depthvar, path2save, ts):
    dayofyr = startDate.timetuple().tm_yday
    daysd = startDate.day
    monthsd = startDate.month
    yearsd = startDate.year
    dayfd = endDate.day
    monthfd = endDate.month
    yearfd = endDate.year
    dayofyrf = endDate.timetuple().tm_yday
    yeardt = yearfd - yearsd
    firstFileName = path + prefix + str(yearsd) +"{0:02d}".format(monthsd)+"{0:02d}".format(daysd)+'12'+sufix
    #print firstFileName

    coords = cutCoords(firstFileName, latvar, lonvar, latbox, lonbox, depths, depthvar, 'hycom')

    latValues = coords[0]
    lonValues = coords[1]
    depthValues = coords[2]
    latminindx = coords[3]
    latmaxindx = coords[4]
    lonminindx = coords[5]
    lonmaxindx = coords[6]

    totalFiles = len(os.listdir(path))
    netcdfsname = [prefix + str(yearsd) +"{0:02d}".format(monthsd)+"{0:02d}".format(daysd)+'12'+'_t'+"{0:03d}".format(indx)+'.nc' for indx in range(0,totalFiles) if indx%ts==0]
    uData = np.zeros((len(netcdfsname), len(depths), len(latValues), len(lonValues)))
    vData = np.zeros((len(netcdfsname), len(depths), len(latValues), len(lonValues)))
    for fileindx in range(0, len(netcdfsname)):
        data = Dataset(path + netcdfsname[fileindx], 'r', format='NETCDF4_CLASSIC')
        var = data.variables
        u = var.get(uvar)
        v = var.get(vvar)
        for depthindx in range(0, len(depths)):
            uData[fileindx, depthindx, :, :] = u[0,depthValues[depthindx], latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
            vData[fileindx, depthindx, :, :] = v[0, depthValues[depthindx], latminindx:latmaxindx + 1,
                                       lonminindx:lonmaxindx + 1]

            tempU = uData[fileindx, depthindx, :, :]
            tempV = vData[fileindx, depthindx, :, :]
            indxU = np.where(tempU == -30000)
            tempU[indxU] = 'NaN'
            tempV[indxU] = 'NaN'

            uData[fileindx, depthindx, :, :] = tempU
            vData[fileindx, depthindx, :, :] = tempV



    fileName = 'hycom_forecast_' + str(yearsd) + "{0:02d}".format(monthsd)+ "{0:02d}".format(daysd)+'_'+str(ts)+'.nc'
    dataset = Dataset(path2save+fileName, 'w', format='NETCDF3_CLASSIC')

    fillValue = 1.267651e+30

    # adding dimensions
    dataset.createDimension('time', None)
    dataset.createDimension('lat', len(latValues))
    dataset.createDimension('lon', len(lonValues))
    dataset.createDimension('depth', len(depths))

    # Adding variables
    time = dataset.createVariable('time', np.float64, ('time',))
    lon = dataset.createVariable('lon', np.float32, ('lon',))
    lat = dataset.createVariable('lat', np.float32, ('lat',))
    depth = dataset.createVariable('depth', np.float32, ('depth',))
    u = dataset.createVariable('u', np.float32, ('time', 'depth', 'lat', 'lon',), fill_value=fillValue)
    v = dataset.createVariable('v', np.float32, ('time', 'depth', 'lat', 'lon',), fill_value=fillValue)

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
    time.units = 'hours since ' + str(yearsd) + '-' + str(monthsd) + '-' + str(daysd) + ' 12:00:00'
    time.standard_name = 'time'

    u.long_name = 'Eastward Water Velocity'
    u.standard_name = 'eastward_sea_water_velocity'
    u.units = 'm/s'

    v.long_name = 'Northward Water Velocity'
    v.standard_name = 'northward_sea_water_velocity'
    v.units = 'm/s'

    timenetcdf = [x for x in range(0, len(netcdfsname)*ts,ts)]
    #print 'timenetcdf: ', timenetcdf
    lat[:] = latValues[:]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]
    depth[:] = depths[:]

    u[:] = uData[:]
    v[:] = vData[:]

    dataset.sync()
    dataset.close()
#startdate = datetime(2020,2,24)
#enddate = datetime(2020,2,24)
#pth = '/DATA/forecastData/hycom/'
#pref = 'hycom_gomu_901m000_'
#suf = '_t000.nc'
#dpth = [0]
#lat = [18.2,31]
#lon = [-98, -81]

#uvar = 'water_u'
#vvar = 'water_v'
#latvar = 'lat'
#lonvar = 'lon'
#depthvar = 'depth'
#path2save = '/DATA/forecastData/Currents/'
#ts = 4
#tic = time.clock()
#hycomforecast_test(startdate, enddate, pth,pref,suf,lat,lon, dpth, uvar,vvar, latvar,lonvar, depthvar, path2save, ts)
#toc = time.clock()
#print(toc-tic)
