import os
from datetime import datetime, timedelta
from gnome import basic_types, scripting, utilities
import numpy as np
from gnome.environment import Water
from os.path import join
import time
import sys
tic = time.clock()
latbox = [18.2, 31]
lonbox = [-98, -80]

#spill timming
now = datetime.today()
start_time = datetime(now.year,now.month, now.day,1)#-timedelta(days=1)
print start_time
duration = timedelta(days=4)
#adding paths
root_repo= '/home/andrea/python/OilSpillForecastSystem/'#'/media/storageBK/Andrea/python/OilSpillForecastSystem/'
forecast_path= join(root_repo, 'pyGnome/forecast')
data_path= '/DATA/forecastData/'#'/media/storageBK/Andrea/python/forecastData/'
today_path = str(start_time.year)+'-'+ "{0:02d}".format(start_time.month)+'-'+ "{0:02d}".format(start_time.day)+'/'
curr_path = 'Currents/'
wind_path = 'Winds/'
map_path = 'BaseMaps/'
sys.path.append(forecast_path)
sys.path.append(join(root_repo,'pyGnome/pre_processing'))
from modelConfigF import make_modelF
from cutcoords import cutCoords
from hycomforecast import hycomforecast
from wrfforecast import wrfforecast
from numb2month import numb2month

#hycom variables for preprocessing data
prefhy = 'hycom_gomu_901m000_'
sufhy = '_t000.nc'

# depths
depths = [0]

#netcdf variables
uvarhy = 'water_u'
vvarhy = 'water_v'
latvarhy = 'lat'
lonvarhy = 'lon'
depthvarhy = 'depth'

path2savehy = join(data_path, curr_path)
#WRF variables for preprocessing data
prefw = 'wrfout_d01_'
sufw= '_00.nc'
latvarw = 'XLAT'
lonvarw = 'XLONG'
uvarw = 'U10'
vvarw = 'V10'
path2savew = join(data_path, wind_path)
wpath = 'wrf/'+"{0:02d}".format(start_time.month)+'_'+numb2month(start_time.month)+'/'

#pre-proccesing currents and winds data
yest = start_time - timedelta(days=1)
tod_hycomfile = prefhy + str(start_time.year) + "{0:02d}".format(start_time.month)+"{0:02d}".format(start_time.day)+'12_t000.nc'
old_hycomfile = prefhy + str(yest.year) +"{0:02d}".format(yest.month)+"{0:02d}".format(yest.day)+'12_t000.nc'
tod_wrffile =  prefw + str(start_time.year) + "-" +"{0:02d}".format(start_time.month)+'-'+ "{0:02d}".format(start_time.day)+sufw
tod_poshycomfile = 'hycom_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
tod_poswrffile =  'WRF_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'

if os.path.exists(join(data_path,curr_path,tod_poshycomfile)):
    currFile = 'hycom_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'

if not os.path.exists(join(data_path,curr_path, tod_poshycomfile)) and not os.path.exists(join(data_path,'hycom/',tod_hycomfile)):
    'using old hycom files'
    duration = duration - timedelta(days=1)
    currFile = 'hycom_forecast'+str(yest.year)+ "{0:02d}".format(yest.month)+ "{0:02d}".format(yest.day)+'.nc'

else:
    hycomforecast(start_time, start_time+timedelta(days=5),join(data_path, 'hycom/') ,prefhy,sufhy,latbox,lonbox, depths, uvarhy,vvarhy, latvarhy,lonvarhy, depthvarhy, path2savehy)
    currFile = 'hycom_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
if os.path.exists(join(data_path,wind_path,tod_poswrffile)):
    windFile = 'WRF_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
elif os.path.exists(join(data_path,wpath,tod_wrffile))==False:
    print join(data_path,wpath,tod_wrffile)
    print 'using old wrf files'
    windFile = 'WRF_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day-1)+'.nc'
    if duration > timedelta(days=3):
        duration = timedelta(days=3)
else:
        wrfforecast(start_time, start_time+timedelta(days=5), join(data_path,wpath),prefw, sufw, latbox, lonbox, uvarw, vvarw, latvarw, lonvarw, path2savew)
        windFile = 'WRF_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
toc = time.clock()
print toc-tic
