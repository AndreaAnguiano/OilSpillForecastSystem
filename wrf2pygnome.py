from netCDF4 import Dataset
from datetime import datetime
import numpy as np
import pandas as pd


def wrf2pygnome(startDate, endDate, path, prefix, lat, lon):
    # se obtienen los valores de la fecha#
    daysd = startDate.day
    monthsd = startDate.month
    yearsd = startDate.year
    dayfd = endDate.day
    monthfd = endDate.month
    yearfd = endDate.year
    dayofyrf = endDate.timetuple().tm_yday
    yeardt = yearfd - yearsd
    coordsFile = path + 'wrfout_c15d_d01_' + str(yearsd) + "-" + "{0:02d}".format(01)+ "-" + "{0:02d}".format(01)+'_00:00:00.'+ str(2010)
    #lastFileName = path + prefix + str(yearsd + yeardt) + "_" + "{0:03d}".format(dayofyrf) + sufix
    #print 'firstFileName:', coordsFile#, '    ', 'lastFileName:', lastFileName

    coordsFile = Dataset(coordsFile, 'r', format='NETCDF4_CLASSIC')
    coordsVar = coordsFile.variables
    latValues = coordsVar.get('XLAT')[0,:,:]
    lonValues = coordsVar.get('XLONG')[0,:,:]


    latmin = [x for x in latValues[:,0] if x <= lat[0]][-1]
    latmax = [x for x in latValues[:,0] if x >= lat[1]][0]
    lonmin = [x for x in lonValues[0,:] if x <= lon[0]][-1]
    lonmax = [x for x in lonValues[0,:] if x >= lon[1]][0]
    latminindx = np.where(latValues == latmin)[0][0]
    latmaxindx = np.where(latValues == latmax)[0][0]
    lonminindx = np.where(lonValues[0] == lonmin)[0][0]
    lonmaxindx = np.where(lonValues[0] == lonmax)[0][0]
    lonValuestemp = lonValues[0]

    lonValues = lonValuestemp[lonminindx:lonmaxindx + 1]
    latValues = latValues[latminindx:latmaxindx+1]



    netcdfsname = [prefix + str(yearsd) + "-" + "{0:02d}".format(monthsd)+ "-" + "{0:02d}".format(daysd)+'_00:00:00.'+ str(yearsd) for date in
                   pd.date_range(startDate, endDate)]

    uData = np.zeros((len(netcdfsname*24), len(latValues), len(lonValues)))
    vData = np.zeros((len(netcdfsname*24), len(latValues), len(lonValues)))

    indtemp = 0
    for fileindx in range(0, len(netcdfsname)):

        data = Dataset(path + netcdfsname[fileindx/24], 'r', format='NETCDF4_CLASSIC')
        var = data.variables
        u = var.get('U10')
        v = var.get('V10')
        for hour in range(0,24):
            uData[indtemp, :, :] = u[hour,latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
            vData[indtemp, :, :] = v[hour,latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
            indtemp += 1


    fileName = 'WRF_' + str(yearsd) + "{0:02d}".format(monthsd) + str(daysd) + '-' + str(yearfd) + "{0:02d}".format(
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

    timenetcdf = [x for x in range(1, len(netcdfsname*24) + 1)]

    lat[:] = latValues[:,0]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]
    u[:] = uData[:]
    v[:] = vData[:]

    dataset.sync()
    dataset.close()



startdate = datetime(2010,04,22)
enddate = datetime(2010,05,22)
pth = '/DATA/petroleo/Datos/WRF_2010/'
pref = 'wrfout_c1h_d01_'
dpth = [0, 100]
lat = [25, 31]
lon = [-92, -80]

import time

tic = time.clock()

wrf2pygnome(startdate, enddate, pth, pref, lat, lon)
toc = time.clock()
print(toc - tic)
