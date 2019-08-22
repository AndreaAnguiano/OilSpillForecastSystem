from plotparticlesforecast import plotparticlesforecast
from datetime import datetime, timedelta
from os.path import join
import cartopy.crs as ccrs
import os
import time
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

import matplotlib.image as image
from post_gnome import nc_particles
from post_gnome.plotting import geo_plots
reload(geo_plots)
import scipy.stats as st


tic = time.clock()
latbox = [17, 31]
lonbox = [-98, -80]
proj=ccrs.PlateCarree()
levels=[0.1, 0.4, 0.8, 1]
output_test='/home/andrea/python/outputs/test_output.nc'
output_test2 = '/DATA/forecastData/Output/2019-06-12/P1/output.nc'
particles = nc_particles.Reader(output_test)
particles2 = nc_particles.Reader(output_test2)
times2 = particles2.times
times = particles.times
tnew = datetime(2019,06,14)
dt = [np.abs(((output_t - tnew).total_seconds())/3600) for output_t in times]
dt2 = [np.abs(((output_t2 -tnew).total_seconds())/3600) for output_t2 in times2]
tidx2 = dt2.index(min(dt2))
tidx = dt.index(min(dt))
TheData2 = particles2.get_timestep(tidx2, variables=['latitude', 'longitude', 'status_codes', 'depth'])
status2 = TheData2['status_codes']
pid2 = np.where(status2==2)[0]
x2 = TheData2['longitude'][pid2]
y2 = TheData2['latitude'][pid2]
TheData = particles.get_timestep(tidx,variables=['latitude','longitude','status_codes','depth'])
status = TheData['status_codes']
pid = np.where(status==2)[0]
x = TheData['longitude'][pid]
y = TheData['latitude'][pid]

xx, yy = np.mgrid[min(x) - .1:max(x) + 100j, min(y)-.1:max(y)+.1:100j]
xx2, yy2 = np.mgrid[min(x) - .1:max(x) + 100j, min(y)-.1:max(y)+.1:100j]

#print min(x),min(x2), max(x),max(x2), min(y),min(y2), max(y), max(y2)
#print xx.shape, xx2.shape, yy.shape, yy2.shape
positions2 = np.vstack([xx2.ravel(),yy.ravel()])
positions = np.vstack([xx.ravel(), yy.ravel()])
#print positions.shape, positions2.shape
values = np.vstack([x,y])
values2 = np.vstack([x2,y2])
kernel = st.gaussian_kde(values2)
f2 = np.reshape(kernel2(positions2).T, xx2.shape)
max_density2 = f2.max()
kernel = st.gaussian_kde(values)
f = np.reshape(kernel(positions).T, xx.shape)
max_density = f.max()
levels.sort()
particle_contours = [lev * max_density for lev in levels]

#adding paths
fig=plt.figure(figsize=(10,5), frameon=False)
ax = plt.subplot(1,1,1,projection=proj)
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
ax.add_feature(coastline,
        edgecolor='black',
        zorder=6,)
ax.add_feature(land,
            zorder=6,)
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
ax.set_title('testttttt', {'fontsize': 15}, 'center')
ax.contour(xx, yy, f, particle_contours, transform=ccrs.PlateCarree())
#plt.tight_layout()
plt.savefig('test.png', bbox_inches = 'tight', pad_inches = 0.1, quality=95)
plt.clf()
plt.close()

