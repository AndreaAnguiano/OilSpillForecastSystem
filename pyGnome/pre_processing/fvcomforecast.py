from netCDF4 import Dataset
import numpy as np
import pandas as pd


def fvcomforecast(startDate, endDate, path, fileName, latbox, lonbox, depths, uvar, vvar, latvar, lonvar, depthvar, path2save, grid_path):
    daysd = startDate.day
    monthsd = startDate.month
    yearsd = startDate.year
    data = Dataset(path + fileName, 'r', format='NETCDF4_CLASSIC')
    nbeData = np.array(pd.read_csv(grid_path+'nbe_forecast.txt', sep=",", header=None).T)
    bndData = np.array(pd.read_csv(grid_path+'bnd_forecast.txt', sep=",", header=None))
    var = data.variables
    u = var.get(uvar)
    v = var.get(vvar)
    latValues = var.get(latvar)
    lonValues = var.get(lonvar)
    timenetcdf = var.get('time')
    nvData = var.get('nv')
    newfileName = 'fvcom_forecast_' + str(yearsd) + "{0:02d}".format(monthsd) + "{0:02d}".format(daysd)+'.nc'
    dataset = Dataset(path2save+newfileName, 'w', format='NETCDF3_CLASSIC')
    uData = u[:, 0, :]
    vData = v[:, 0, :]
    fillValue = 1.267651e+30

    # adding dimensions
    dataset.createDimension('time', None)
    dataset.createDimension('node', latValues.shape[0])
    dataset.createDimension('nele', uData.shape[1])
    dataset.createDimension('three', 3)
    dataset.createDimension('nbnd', bndData.shape[0])
    dataset.createDimension('nbi', 4)

    # Adding variables
    time = dataset.createVariable('time', np.float32, ('time',))
    lon = dataset.createVariable('lon', np.float32, ('node',))
    lat = dataset.createVariable('lat', np.float32, ('node',))
    u = dataset.createVariable('u', np.float32, ('time', 'nele',), fill_value=fillValue)
    v = dataset.createVariable('v', np.float32, ('time', 'nele',), fill_value=fillValue)
    nv = dataset.createVariable('nv', np.int32, ('three', 'nele',))
    bnd = dataset.createVariable('bnd', np.int32, ('nbnd', 'nbi',))
    nbe = dataset.createVariable('nbe', np.int32, ('three', 'nele',))
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
    time.time_zone = 'UTC'
    time.format = 'defined reference date'

    u.long_name = 'Eastward Water Velocity'
    u.standard_name = 'eastward_sea_water_velocity'
    u.units = 'm/s'
    #u.coordinates = 'time siglay latc lonc'
    #u.mesh = 'fvcom_mesh'
    #u.grid = 'fvcom_grid'
    #u.location = 'face'
    #u.type = 'data'

    v.long_name = 'Northward Water Velocity'
    v.standard_name = 'northward_sea_water_velocity'
    v.units = 'm/s'
    #v.coordinates = 'time siglay latc lonc'
    #v.mesh = 'fvcom_mesh'
    #v.grid = 'fvcom_grid'
    #v.location = 'face'
    #v.type = 'data'

    #nbe.order = 'cw'
    nv.lon_name = 'nodes surrounding element'
    lat[:] = latValues[:]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]

    u[:] = uData[:]
    v[:] = vData[:]
    nv[:] = nvData[:]
    bnd[:] = bndData[:]
    nbe[:] = nbeData[:]

    dataset.sync()
    dataset.close()





#startdate = datetime(2019,8,19)
#enddate = datetime(2019,8,19)
#pth = '/DATA/forecastData/fvcom/'
#pref = 'Sargazo04_'
#latbox = [16, 17]
#lonbox = [274, 272]
#suf= '_sup.nc'
#depths= [0]
#latvar = 'lat'
#lonvar = 'lon'
#uvar = 'u'
#vvar = 'v'
#path2save = '/home/andrea/python/OilSpillForecastSystem/pyGnome/pre_processing/'
#fileName = pth+pref+'0001'+suf
#depthvar = 'siglay'
#model = 'fvcom'
#fvcomforecast(startdate,enddate,pth,pref,suf,latbox,lonbox,depths, uvar,vvar, latvar, lonvar, depthvar,path2save)
