from netCDF4 import Dataset
from datetime import datetime
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
def cutCoords(fileName,latvar,lonvar, latbox, lonbox, depths, depthvar, model):

    coordsFile = Dataset(fileName, 'r', format='NETCDF4_CLASSIC')
    coordsVar = coordsFile.variables
    latValues = coordsVar.get(latvar)
    lonValues = coordsVar.get(lonvar)
    if model == 'hycom':
        latmin = [x for x in latValues if x <= latbox[0]][-1]
        latmax = [x for x in latValues if x >= latbox[1]][0]

        latValues = latValues[np.where(latValues == latmin)[0][0]:np.where(latValues == latmax)[0][0] + 1]

        lonmin = [x for x in lonValues if x <= lonbox[0]][-1]
        lonmax = [x for x in lonValues if x >= lonbox[1]][0]

        lonValues = lonValues[np.where(lonValues == lonmin)[0][0]:np.where(lonValues == lonmax)[0][0] + 1]

        latminindx = np.where(latValues == latmin)[0][0]
        latmaxindx = np.where(latValues == latmax)[0][0]
        lonminindx = np.where(lonValues == lonmin)[0][0]
        lonmaxindx = np.where(lonValues == lonmax)[0][0]

        depthValues = coordsVar.get(depthvar)
        depthmin = [x for x in depthValues if x == depths[0]][0]
        depthmax = [x for x in depthValues if x == depths[-1]][0]
        depthValues = depthValues[np.where(depthValues == depthmin)[0][0]:np.where(depthValues == depthmax)[0][0] + 1]
        return [latValues, lonValues,depthValues, latminindx, latmaxindx, lonminindx, lonmaxindx]
    elif  model=='wrf':
        latValues = latValues[0,:,:]
        lonValues = lonValues[0,:,:]
        #print 'latshape: ', latValues.shape, 'lonShape: ', lonValues.shape
        #print 'latvalues', latValues[:,0]
        #print 'lonvalues', lonValues[0,:]
        latmin = [x for x in latValues[:,0] if x <= latbox[0]][-1]
        latmax = [x for x in latValues[:,0] if x >= latbox[1]][0]
        lonmin = [x for x in lonValues[0,:] if x <= lonbox[0]][-1]
        lonmax = [x for x in lonValues[0,:] if x >= lonbox[1]][0]
        #print 'latmin: ', latmin,'latmax: ',latmax, 'lonmin: ', lonmin, 'lonmax: ', lonmax
        latminindx = np.where(latValues == latmin)[0][0]
        latmaxindx = np.where(latValues == latmax)[0][0]
        lonminindx = np.where(lonValues[0] == lonmin)[0][0]
        lonmaxindx = np.where(lonValues[0] == lonmax)[0][0]
        #print 'latminindx: ', latminindx, 'latmaxindx: ', latmaxindx, 'lonminxindx: ', lonminindx, 'lonmaxindx: ', lonmaxindx
        #print 'lenlat: ',  latmaxindx-latminindx, 'lenlon: ', lonmaxindx-lonminindx
        lonValuestemp = lonValues[0]
        latValuestemp = latValues[:,0]
        #print 'lonValuestemp: ', lonValuestemp

        lonValues = lonValuestemp[lonminindx:lonmaxindx + 1]
        latValues = latValuestemp[latminindx:latmaxindx+1]
        #print 'final_lat: ', latValues.shape,latValues, 'final_lon: ', lonValues.shape, lonValues
        return [latValues, lonValues, latminindx, latmaxindx, lonminindx, lonmaxindx]


#startdate = datetime(2019,8,19)
#enddate = datetime(2019,8,19)
#pth = '/DATA/forecastData/fvcom/'
#pref = 'Sargazo04_'
#latbox = [16, 17]
#lonbox = [274, 272]
#suf= '_sup.nc'
#depths= 0
#latvar = 'lat'
#lonvar = 'lon'
#uvar = 'u'
#vvar = 'v'
#path2save = '/DATA/forecastData/test/'
#fileName = pth+pref+'0001'+suf
#depthvar = 'siglay'
#model = 'fvcom'
#cutCoords(fileName,latvar,lonvar, latbox, lonbox, depths, depthvar, model)
