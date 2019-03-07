from netCDF4 import Dataset
from datetime import datetime
import numpy as np
import pandas as pd
import math as m


def wrfedit2pygnome(startDate, endDate, path, prefix,sufix, lat, lon,uvar, vvar, latvar,lonvar):
    # se obtienen los valores de la fecha#
    dayofyr = startDate.timetuple().tm_yday
    daysd = startDate.day
    monthsd = startDate.month
    yearsd = startDate.year
    dayfd = endDate.day
    monthfd = endDate.month
    yearfd = endDate.year
    dayofyrf = endDate.timetuple().tm_yday
    yeardt = yearfd - yearsd
    coordsFile = path + prefix + str(yearsd) + "_" + str(dayofyr)+'_1'+sufix
    #lastFileName = path + prefix + str(yearsd + yeardt) + "_" + "{0:03d}".format(dayofyrf) + sufix
    #print 'firstFileName:', coordsFile#, '    ', 'lastFileName:', lastFileName

    coordsFile = Dataset(coordsFile, 'r', format='NETCDF4_CLASSIC')
    coordsVar = coordsFile.variables
    latValues = coordsVar.get(latvar)
    lonValues = coordsVar.get(lonvar)


    latmin = [x for x in latValues if x <= lat[0]][-1]
    latmax = [x for x in latValues if x >= lat[1]][0]
    lonmin = [x for x in lonValues if x <= lon[0]][-1]
    lonmax = [x for x in lonValues if x >= lon[1]][0]
    latminindx = np.where(latValues == latmin)[0][0]
    latmaxindx = np.where(latValues == latmax)[0][0]
    lonminindx = np.where(lonValues == lonmin)[0][0]
    lonmaxindx = np.where(lonValues == lonmax)[0][0]


    lonValues = lonValues[lonminindx:lonmaxindx + 1]
    latValues = latValues[latminindx:latmaxindx+1]

    netcdfsname = [
        [prefix + str(date.year) + "_" + "{0:03d}".format(date.timetuple().tm_yday) +'_'+ str(val) + sufix for val in
         range(1, 5)] for date in pd.date_range(startDate, endDate)]

    uData = np.zeros((len(netcdfsname)*4, len(latValues), len(lonValues)))
    vData = np.zeros((len(netcdfsname)*4, len(latValues), len(lonValues)))

    indtemp = 0
    for fileindx in range(0, len(netcdfsname)):
        for hour in range(0,4):
            data = Dataset(path + netcdfsname[fileindx][hour], 'r', format='NETCDF4_CLASSIC')
            var = data.variables
            u = var.get(uvar)
            v = var.get(vvar)

            uData[indtemp, :, :] = u[latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
            vData[indtemp, :, :] = v[latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
            indtemp += 1





    fileName = 'WRF_v3_' + str(yearsd) + "{0:02d}".format(monthsd) + str(daysd) + '-' + str(yearfd) + "{0:02d}".format(
        monthfd) + str(dayfd) + '.nc'
    dataset = Dataset('Data/' + fileName, 'w', format='NETCDF3_CLASSIC')

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

    timenetcdf = [x for x in range(0, len(netcdfsname)*24+1,6)]

    lat[:] = latValues[:]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]
    u[:] = uData[:]
    v[:] = vData[:]

    dataset.sync()
    dataset.close()



startdate = datetime(2010,04,22)
enddate = datetime(2010,05,11)
pth = '/DATA/proyectos_Julio_Lara/WRF_2010/'
pref = 'WRF_'
dpth = [0, 100]
lat = [18.2, 31]
lon = [-98, -83]
suf= '.nc'
latvar = 'Latitud'
lonvar = 'Longitud'
uvar = 'U_Viento'
vvar = 'V_Viento'

import time

tic = time.clock()

wrfedit2pygnome(startdate, enddate, pth,pref, suf, lat, lon,uvar, vvar, latvar,lonvar)
toc = time.clock()
print(toc - tic)
