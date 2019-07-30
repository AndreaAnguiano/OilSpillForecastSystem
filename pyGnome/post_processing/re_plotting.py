from plotparticlesforecast import plotparticlesforecast
from datetime import datetime, timedelta
from os.path import join
import cartopy.crs as ccrs
import os
import time
tic = time.clock()
namePosition = ['P1', 'P2', 'P3', 'P4', 'P5','P6']
coords = [[-95.01622889, 25.97096444],[-95.25811667, 25.36115583], [-96.56495556, 24.75155556],[- 96.82528583, 23.51224639],[-96.71577028, 20.97098889],[-94.76735833, 20.04058889]]
latbox = [17, 31]
lonbox = [-98, -80]
#spill timming
#now = datetime(2019,07,9)
#start_time = datetime(now.year,now.month, now.day,1)-timedelta(days=1)
for i in range(0,2):
    start_time =datetime(2019,7,23)+timedelta(days=i)
#adding paths
    data_path= '/DATA/forecastData/'#'/media/storageBK/Andrea/python/forecastData/'
    today_path = str(start_time.year)+'-'+ "{0:02d}".format(start_time.month)+'-'+ "{0:02d}".format(start_time.day)+'/'
    filenameplot = 'output.nc'
    dt = 1
    proj=ccrs.PlateCarree()
    for indx in range(0,6):
            print 'running ', namePosition[indx], ' position', coords[indx]
            daily_output_path = os.path.dirname(join(data_path,'Output/', today_path, namePosition[indx]+'/'))
            print daily_output_path
            if not os.path.exists(daily_output_path):
                os.mkdir(daily_output_path)
                print("Daily directory created ")
            else:
                print("Daily directory already exists")
            plotparticlesforecast(daily_output_path, namePosition[indx], filenameplot, start_time, dt,latbox,lonbox, proj)
    toc = time.clock()
    print toc-tic
