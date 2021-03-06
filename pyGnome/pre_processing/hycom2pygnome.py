from netCDF4 import Dataset
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def hycom2pygnome(startDate, endDate, path,prefix,sufix,lat,lon, depths, uvar,vvar, latvar,lonvar, depthvar):
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
    firstFileName = path + prefix + str(yearsd) + "_" + "{0:03d}".format(dayofyr) + sufix
    # print 'firstFileName:', firstFileName, '    ', 'lastFileName:', lastFileName

    coordsFile = Dataset(firstFileName, 'r', format='NETCDF4_CLASSIC')
    coordsVar = coordsFile.variables
    latValues = coordsVar.get(latvar)
    lonValues = coordsVar.get(lonvar)
    depthValues = coordsVar.get(depthvar)

    latmin = [x for x in latValues if x <= lat[0]][-1]
    latmax = [x for x in latValues if x >= lat[1]][0]

    latValues = latValues[np.where(latValues == latmin)[0][0]:np.where(latValues == latmax)[0][0] + 1]

    lonmin = [x for x in lonValues if x <= lon[0]][-1]
    lonmax = [x for x in lonValues if x >= lon[1]][0]

    lonValues = lonValues[np.where(lonValues == lonmin)[0][0]:np.where(lonValues == lonmax)[0][0] + 1]

    depthmin = [x for x in depthValues if x == depths[0]][0]
    depthmax = [x for x in depthValues if x == depths[-1]][0]

    depthValues = depthValues[np.where(depthValues == depthmin)[0][0]:np.where(depthValues == depthmax)[0][0] + 1]
    # print depthValues[:]
    latminindx = np.where(latValues == latmin)[0][0]
    latmaxindx = np.where(latValues == latmax)[0][0]
    lonminindx = np.where(lonValues == lonmin)[0][0]
    lonmaxindx = np.where(lonValues == lonmax)[0][0]
    netcdfsname = [prefix + str(date.year) + "_" + "{0:03d}".format(date.timetuple().tm_yday) + sufix for date in
                   pd.date_range(startDate, endDate)]
    uData = np.zeros((len(netcdfsname), len(depths), len(latValues), len(lonValues)))
    vData = np.zeros((len(netcdfsname), len(depths), len(latValues), len(lonValues)))
    print len(latValues), len(lonValues)
    netcdfsname = [prefix + str(date.year) + "_" + "{0:03d}".format(date.timetuple().tm_yday) + sufix for date in
                   pd.date_range(startDate, endDate)]
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

            #print tempU[0,0,:,:]
            #plt.imshow(vData[0,0,:,:])#u[0,0,latminindx:latmaxindx,lonminindx:lonmaxindx + 1])
            #plt.show()

    fileName = 'hycom_v4_' + str(yearsd) + "{0:02d}".format(monthsd) + str(daysd) + '-' + str(yearfd) + "{0:02d}".format(monthfd) + str(dayfd) + '.nc'
    dataset = Dataset('Data/' + fileName, 'w', format='NETCDF3_CLASSIC')

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
    time.units = 'days since ' + str(yearsd) + '-' + str(monthsd) + '-' + str(daysd-1) + ' 00:00:00'
    time.standard_name = 'time'

    u.long_name = 'Eastward Water Velocity'
    u.standard_name = 'eastward_sea_water_velocity'
    u.units = 'm/s'

    v.long_name = 'Northward Water Velocity'
    v.standard_name = 'northward_sea_water_velocity'
    v.units = 'm/s'

    timenetcdf = [x for x in range(1, len(netcdfsname) + 1)]

    lat[:] = latValues[:]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]
    depth[:] = depths[:]

    u[:] = uData[:]
    v[:] = vData[:]

    dataset.sync()
    dataset.close()



startdate = datetime(2010,04,22)
enddate = datetime(2010,05,22)
pth = '/DATA/proyectos_Julio_Lara/HYCOM_2010_50p1/'
pref = 'hycom_gomu_501_'
suf = '_t000.nc'
dpth = [0]
lat = [18.2,31]
lon = [-98, -81]

uvar = 'water_u'
vvar = 'water_v'
latvar = 'lat'
lonvar = 'lon'
depthvar = 'depth'
import time

tic = time.clock()
hycom2pygnome(startdate,enddate,pth,pref,suf,lat,lon,dpth, uvar,vvar, latvar,lonvar, depthvar)
toc = time.clock()
print(toc-tic)
