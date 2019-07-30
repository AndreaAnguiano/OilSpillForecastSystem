import os
from os.path import join
from scipy.io import loadmat
from datetime import datetime, timedelta
from calendar import monthrange
import numpy as np
import scipy.io as sio
from netCDF4 import Dataset, num2date
import matplotlib.pyplot as plt
import matplotlib
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

def plotparticlesforecast(data_path, point, filename, t, dts, latbox,lonbox, proj):
   # plt.clf()
#data_path = '/DATA/forecastData/'
#output_test='/DATA/forecastData/Output/2019-06-11/P2/output.nc'
    
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
    for i in np.arange(0,len(times[:]),dts):
        tnew =t + timedelta(hours=i)
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
        ax.set_title(str(tnew)+point, {'fontsize': 15}, 'center')
        plotScatter = plt.scatter(TheData['longitude'][pid],TheData['latitude'][pid],s=3,color='k',marker='.')
        plt.savefig(data_path+'/'+'foreground_'+"{0:05d}".format(i)+'.png', bbox_inches = 'tight', pad_inches = 0.1, quality=95)
        plt.clf()
        plt.close()