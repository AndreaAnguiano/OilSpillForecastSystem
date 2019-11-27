from mainF import main
import os
from datetime import datetime, timedelta
from os.path import join
import time
import sys
import cartopy.crs as ccrs
namePosition = ['P1', 'P2', 'P3', 'P4', 'P5','P6']
coords = [[-95.01622889, 25.97096444], [-95.25811667, 25.36115583], [-96.56495556, 24.75155556], [- 96.82528583, 23.51224639], [-96.71577028, 20.97098889], [-94.76735833, 20.04058889]]
latbox = [18.2, 31]
lonbox = [-98, -83]
# spill timming
now = datetime.today()
start_time = datetime(now.year, now.month, now.day, 1)  # -timedelta(days=1)
print start_time
duration = timedelta(days=4)
# adding paths
root_repo = '/media/storageBK/Andrea/python/OilSpillForecastSystem/'
forecast_path = join(root_repo, 'pyGnome/forecast')
data_path = '/media/storageBK/Andrea/python/forecastData/'
today_path = str(start_time.year)+'-' + "{0:02d}".format(start_time.month)+'-' + "{0:02d}".format(start_time.day) + '/'
output_path = '/var/www/html/OilSpill_Forecast/images/'
curr_path = 'Currents/'
wind_path = 'Winds/'
map_path = 'BaseMaps/'

if not os.path.exists(output_path+today_path):
    os.mkdir(output_path+today_path)
    print("Daily directory created ")
else:
    print("Daily directory already exists")
from numb2month import numb2month

# hycom variables for preprocessing data
prefhy = 'hycom_gomu_901m000_'
sufhy = '_t000.nc'

# depths
depths = [0]

# netcdf variables
uvarhy = 'water_u'
vvarhy = 'water_v'
latvarhy = 'lat'
lonvarhy = 'lon'
depthvarhy = 'depth'
path2savehy = join(data_path, curr_path)
# WRF variables for preprocessing data
prefw = 'wrfout_d01_'
sufw = '_00.nc'
latvarw = 'XLAT'
lonvarw = 'XLONG'
uvarw = 'U10'
vvarw = 'V10'
path2savew = join(data_path, wind_path)
wpath = 'wrf/'+"{0:02d}".format(start_time.month)+'_'+numb2month(start_time.month)+'/'
# Plot settings
sys.path.append(join(root_repo, 'pyGnome/post_processing'))

from plotparticlesforecast import plotparticlesforecast
proj = ccrs.PlateCarree()
dt = 1
filenameplot = 'output.nc'
for indx in range(0, len(namePosition)):
        print 'running ', namePosition[indx], ' position', coords[indx]
        daily_output_path = os.path.dirname(join(output_path, today_path, namePosition[indx]+'/'))
        if not os.path.exists(daily_output_path):
            os.mkdir(daily_output_path)
            print("Daily directory created ")
        else:
            print("Daily directory already exists")

        main(coords[indx], namePosition[indx], latbox, lonbox, start_time, duration,
        root_repo, forecast_path, data_path, daily_output_path, curr_path, wind_path,
        map_path, prefhy, sufhy, depths, uvarhy, vvarhy, latvarhy, lonvarhy, depthvarhy,
        path2savehy, prefw, sufw, latvarw, lonvarw, uvarw, vvarw, path2savew, wpath)
        tic = time.clock()
        plotparticlesforecast(daily_output_path, namePosition[indx], filenameplot,
        start_time, dt, latbox, lonbox, proj)
        toc = time.clock()
        print toc-tic
