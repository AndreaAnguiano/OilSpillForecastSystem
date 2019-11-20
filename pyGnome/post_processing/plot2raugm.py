import os
from os.path import join
from scipy.io import loadmat
from datetime import datetime, timedelta
from calendar import monthrange
import numpy as np
import scipy.io as sio
from netCDF4 import Dataset, num2date
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.switch_backend('agg')
from pylab import figure, cm
from cartopy import feature
import cartopy.crs as ccrs
import cartopy.vector_transform as cvt
from cartopy.feature import NaturalEarthFeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from cartopy.io.shapereader import Reader
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.image as image
from post_gnome import nc_particles
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def plotraugm(data_path, point, filename, t, dts, latbox,lonbox, proj):
   # plt.clf()
#data_path = '/DATA/forecastData/'
#output_test='/DATA/forecastData/Output/2019-06-11/P2/output.nc'
    currfile = '/DATA/forecastData/Currents/hycom_forecast_20191022.nc'
    dataset = Dataset(currfile, 'r', format='NETCDF4_CLASSIC')
    var = dataset.variables
    lat = var.get('lat')[:]
    lon = var.get('lon')[:]
    
    particles = nc_particles.Reader(data_path+'/'+filename)
    times = particles.times
    states = NaturalEarthFeature(category="cultural", scale="10m",
            facecolor="none",
            name='admin_1_states_provinces_lines')
    coastline = NaturalEarthFeature(category="physical", scale="10m",
            facecolor="none",
            name='coastline')
    land = NaturalEarthFeature(category="physical", scale="10m",
            facecolor='lightgray',
            name='land',)
    latmin=latbox[0]
    latmax=latbox[1]
    lonmin=lonbox[0]
    lonmax=lonbox[1]
    lol = 0
    for i in np.arange(0,len(times[:])+1,24):
        print lol
        tnew =t + timedelta(hours=i)
        u = var.get('u')[lol,0,:,:]
        v = var.get('v')[lol,0,:,:]
        mag = np.sqrt(u**2+v**2)

        #print tnew, '   ', i
        dt = [np.abs(((output_t - tnew).total_seconds())/3600) for output_t in times]
        tidx = dt.index(min(dt))
        TheData = particles.get_timestep(tidx,variables=['latitude','longitude','status_codes','depth'])
        status = TheData['status_codes']
        pid = np.where(status==2)[0]
        fig=plt.figure(figsize=(10,5))
        #fig.subplots_adjust(left=0.125,right=0.9,top=0.95,bottom=0.1)
        ax = plt.subplot(1,1,1,
            projection=proj)
        ax.add_feature(coastline,
        edgecolor='black',
        zorder=6,)
        ax.add_feature(land,
            zorder=10,)
        ax.add_feature(states,
        edgecolor='gray',
        zorder=12,)
        ax_leg=ax.gridlines(
            draw_labels=True,linewidth=0.5,
            linestyle='--')
        ax_leg.xlabels_top=False
        ax_leg.ylabels_right=False
        ax_leg.xlocator=mticker.FixedLocator(range(int(lonmin),int(lonmax)+2,2))
        ax_leg.xformatter=LONGITUDE_FORMATTER
        ax_leg.ylocator=mticker.FixedLocator(range(int(latmin),int(latmax)+2,2))
        ax_leg.yformatter=LATITUDE_FORMATTER
        ax_leg.xlabel_style = {'size': 10, 'color': 'black'}
        ax_leg.ylabel_style = {'size': 10, 'color': 'black'}
        plt.xlim([lonmin, lonmax])
        plt.ylim([latmin, latmax])
        ubarbs = u[::6, ::6]
        vbarbs = v[::6, ::6]
        lonbarbs = lon[::6]
        latbarbs = lat[::6]

        ax.set_title(str(tnew)+' '+point, {'fontsize': 15}, 'center')
        plt.plot(-95.01622889, 25.97096444, marker='*', color='white',markersize=10)
        cmapm = plt.get_cmap = 'jet'
        cmap= mpl.cm.cool
        cs = plt.pcolormesh(lon, lat,mag, cmap=cmapm)
        plt.quiver(lonbarbs,latbarbs,ubarbs,vbarbs, headwidth=3, headlength=3, width=0.001,color='white')
        plt.scatter(TheData['longitude'][pid],TheData['latitude'][pid],s=10,color='fuchsia',marker='.')
        axins1 = inset_axes(ax, width = '100%', height='2.5%', loc='lower center', borderpad=-3)
        bounds = [0, 0.25, 0.50, 0.75, 1.00, 1.25,1.50,1.75,2]
        ar = fig.colorbar(cs,cax=axins1, orientation='horizontal', ticks=bounds) #,fraction=0.05555)
        cs.set_clim(0,2)
        ar.ax.set_xlabel('Velocidad (m/s)')
        plt.plot([95.01622889, 25.97096444], marker='*', color='red',markersize=12)

        plt.savefig(data_path+'/'+'foreground_'+"{0:05d}".format(i)+'.png', bbox_inches = 'tight', pad_inches = 0.1, quality=95)
        plt.clf()
        plt.close()
        lol= lol+1

namePosition = ['P1', 'P2', 'P3', 'P4', 'P5','P6']
coords = [[-95.01622889, 25.97096444],[-95.25811667, 25.36115583], [-96.56495556, 24.75155556],[- 96.82528583, 23.51224639],[-96.71577028, 20.97098889],[-94.76735833, 20.04058889]]
latbox = [18.2, 31]
lonbox = [-98, -80]
#spill timming
#now = datetime(2019,07,9)
#start_time = datetime(now.year,now.month, now.day,1)-timedelta(days=1)
for i in range(0,1):
    start_time =datetime(2019,10,22)+timedelta(days=i)
#adding paths
    data_path= '/DATA/forecastData/'#'/media/storageBK/Andrea/python/forecastData/'
    today_path = str(start_time.year)+'-'+ "{0:02d}".format(start_time.month)+'-'+ "{0:02d}".format(start_time.day)+'/'
    filenameplot = 'output.nc'
    dt = 1
    proj=ccrs.PlateCarree()
    for indx in range(0,1):
            print 'running ', namePosition[indx], ' position', coords[indx]
            daily_output_path = os.path.dirname(join(data_path,'Output/', today_path, namePosition[indx]+'/'))
            print daily_output_path
            if not os.path.exists(daily_output_path):
                os.mkdir(daily_output_path)
                print("Daily directory created ")
            else:
                print("Daily directory already exists")
            plotraugm(daily_output_path, namePosition[indx], filenameplot, start_time, dt,latbox,lonbox, proj)

