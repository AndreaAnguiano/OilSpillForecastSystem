import mainfvcom
import os
from datetime import datetime, timedelta
from os.path import join
import time
import sys
import cartopy.crs as ccrs

namePosition = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
coords = [[-86.5, 20], [-86, 19.5], [-85.5, 19],
          [-85.5, 18.7], [-87, 18.5], [-87.5, 18.2]]
latbox = [12, 24]
lonbox = [-90, -79]
# spill timming
now = datetime.today()
start_time = datetime(now.year, now.month, now.day, 1)  # -timedelta(days=1)
print start_time
duration = timedelta(days=3)
# adding paths
root_repo = '/home/andrea/python/OilSpillForecastSystem/'  # '/media/storageBK/Andrea/python/OilSpillForecastSystem/'
forecast_path = join(root_repo, 'pyGnome/forecast')
data_path = '/DATA/forecastData/'
today_path = str(start_time.year) + '-' + "{0:02d}".format(start_time.month) + '-' + "{0:02d}".format(
    start_time.day) + '/'
output_path = '/DATA/forecastData/test/'
curr_path = 'Currents_FVCOM/'
wind_path = 'Winds/'
map_path = 'BaseMaps/'

fvcom_today_path = str(start_time.year) + '_' + "{0:02d}".format(start_time.month) + '_' + "{0:02d}".format(
    start_time.day) + '_00' + '/'

if not os.path.exists(output_path + today_path):
    os.mkdir(output_path + today_path)
    print("Daily directory created ")
else:
    print("Daily directory already exists")

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

# Plot settings
sys.path.append(join(root_repo, 'pyGnome/post_processing'))

from plotparticlesforecast import plotparticlesforecast

proj = ccrs.PlateCarree()
dt = 1
filenameplot = 'output.nc'
for indx in range(0, len(namePosition)):

    print 'running ', namePosition[indx], ' position', coords[indx]
    daily_output_path = os.path.dirname(join(output_path, today_path, namePosition[indx] + '/'))
    if not os.path.exists(daily_output_path):
        os.mkdir(daily_output_path)
        print("Daily directory created ")
    else:
        print("Daily directory already exists")

    mainfvcom.mainfvcom(coords[indx], namePosition[indx], latbox, lonbox, start_time, duration,
                        root_repo, forecast_path, data_path, daily_output_path, curr_path, wind_path,
                        map_path, fvcom_fileName, depths, uvarfv, vvarfv, latvarfv, lonvarfv,
                        depthvarfv, path2savefv, prefw, sufw, latvarw, lonvarw, uvarw, vvarw, path2savew, wpath, fvpath,
                        grid_path)

    tic = time.clock()
    plotparticlesforecast(daily_output_path, namePosition[indx], filenameplot, start_time, dt, latbox, lonbox, proj)
    toc = time.clock()
    print toc-tic
