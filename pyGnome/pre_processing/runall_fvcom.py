import os
from datetime import datetime, timedelta
from os.path import join
import time
import sys
tic = time.clock()

latbox = [16, 17]
lonbox = [274, 272]

# spill timming
now = datetime.today()
start_time = datetime(now.year, now.month, now.day, 1)  # -timedelta(days=1)
print start_time
duration = timedelta(days=4)
# adding paths
root_repo = '/home/andrea/python/OilSpillForecastSystem/'#'/media/storageBK/Andrea/python/OilSpillForecastSystem/'
forecast_path = join(root_repo, 'pyGnome/forecast')
data_path = '/DATA/forecastData/'  # '/media/storageBK/Andrea/python/forecastData/'
today_path = str(start_time.year) + '-' + "{0:02d}".format(start_time.month)+'-' + "{0:02d}".format(start_time.day) + '/'
curr_path = 'Currents_FVCOM/'
wind_path = 'Winds/'
map_path = 'BaseMaps/'
fvcom_today_path = str(start_time.year) + '_' + "{0:02d}".format(start_time.month)+'_' + "{0:02d}".format(start_time.day) + '_00' + '/'
sys.path.append(forecast_path)
sys.path.append(join(root_repo, 'pyGnome/pre_processing'))

from fvcomforecast import fvcomforecast
from wrfforecast import wrfforecast
from numb2month import numb2month

# fvcom variables for preprocessing data
fvcom_fileName = 'Sargazo04_0001_sup.nc'
latvarfv = 'lat'
lonvarfv = 'lon'
uvarfv = 'u'
vvarfv = 'v'
depthvarfv = 'siglay'
# depths
depths = [0]
path2savefv = join(data_path, curr_path)
fvpath = join('fvcom/', fvcom_today_path)
grid_path = join(data_path, 'fvcom/', 'grids/')
# WRF variables for preprocessing data
prefw = 'wrfout_d01_'
sufw = '_00.nc'
latvarw = 'XLAT'
lonvarw = 'XLONG'
uvarw = 'U10'
vvarw = 'V10'
path2savew = join(data_path, wind_path)
wpath = 'wrf/' + "{0:02d}".format(start_time.month) + '_' + numb2month(start_time.month) + '/'

# pre-proccesing currents and winds data
yest = start_time - timedelta(days=1)

tod_wrffile = prefw + str(start_time.year) + "-" + "{0:02d}".format(start_time.month)+ '-' + "{0:02d}".format(start_time.day)+ sufw
tod_poswrffile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
print join(data_path, fvpath)
if os.path.exists(join(data_path, fvpath)):
    print 'here'
    fvcomforecast(start_time, start_time + duration, join(data_path, fvpath), fvcom_fileName, latbox, lonbox, depths, uvarfv, vvarfv, latvarfv, lonvarfv, depthvarfv, path2savefv, grid_path)
    currFile = 'fvcom_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
else:
    'using old fvcom files'
    duration = duration - timedelta(days=1)
    currFile = 'fvcom_forecast' + str(yest.year) + "{0:02d}".format(yest.month) + "{0:02d}".format(yest.day) + '.nc'

if os.path.exists(join(data_path, wind_path, tod_poswrffile)):
    windFile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
elif os.path.exists(join(data_path, wpath, tod_wrffile)) is False:
    print join(data_path, wpath, tod_wrffile)
    print 'using old wrf files'
    windFile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day-1)+'.nc'
    if duration > timedelta(days=3):
        duration = timedelta(days=3)

toc = time.clock()
print toc-tic
