# coding: utf-8
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


from mpl_toolkits.axes_grid1.inset_locator import inset_axes
currfile = '/DATA/forecastData/Winds/WRF_forecast_20191022.nc'
dataset = Dataset(currfile, 'r', format='NETCDF4_CLASSIC')
var = dataset.variables
lat = var.get('lat')[:]
lon = var.get('lon')[:]
u = var.get('air_u')[0,:,:]
v = var.get('air_v')[0,:,:]
mag = np.sqrt(u**2+v**2)
proj=ccrs.PlateCarree()
namePosition = ['P1', 'P2', 'P3', 'P4', 'P5','P6']
coords = [[-95.01622889, 25.97096444],[-95.25811667, 25.36115583], [-96.56495556, 24.75155556],[- 96.82528583, 23.51224639],[-96.71577028, 20.97098889],[-94.76735833, 20.04058889]]

lons = [coords[i][0] for i in range(0,len(coords))]
lats = [coords[i][1] for i in range(0,len(coords))]
latbox = [18.2, 31]
lonbox = [-98, -80]
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

fig=plt.figure(figsize=(10,5))
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
ax_leg=ax.gridlines(draw_labels=True,linewidth=0.001,linestyle='--')
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
cmap = plt.get_cmap = 'Blues'
cs = plt.contourf(lon,lat,mag,cmap=cmap)
#cs = plt.pcolormesh(lon, lat,mag, cmap=cmap)
ubarbs = u[::6, ::6]
vbarbs = v[::6, ::6]
lonbarbs = lon[::6]
latbarbs = lat[::6]
print u.shape, ubarbs.shape
plt.barbs(lonbarbs,latbarbs,ubarbs,vbarbs, linewidth=0.3, length=5)
#plt.quiver(lonbarbs,latbarbs,ubarbs,vbarbs, headwidth=3, headlength=3, width=0.001)
plt.title('Modelo WRF 22/10/2019 00:00 GMT \nViento en superficie', loc='left', fontsize=8)
plt.title(u'Pronóstico a 00 hrs\nHora local CDMX 19:00 21/10/2019', loc='right', fontsize=8)
axins1 = inset_axes(ax, width = '100%', height='2.5%', loc='lower center', borderpad=-3)
cbar = fig.colorbar(cs,cax=axins1, orientation='horizontal') #,fraction=0.05555)
cbar.ax.set_xlabel('Intensidad del viento (m/s)')
plt.savefig('winds_test.png', bbox_inches = 'tight', pad_inches = 0.1, quality=95)
plt.clf()
plt.close()

