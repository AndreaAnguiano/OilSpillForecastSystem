
import os
from os.path import join
from scipy.io import loadmat
from datetime import datetime, timedelta
from calendar import monthrange
import numpy as np
import scipy.io as sio
from netCDF4 import Dataset, num2date
import matplotlib.pyplot as plt
from pylab import figure, cm
from matplotlib.colors import LogNorm
from post_gnome.plotting import geo_plots
reload(geo_plots)
from post_gnome import nc_particles
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

data_path = '/DATA/forecastData/'
output_test='/DATA/forecastData/Output/2019-06-11/P2/output.nc'
for i in range(1,72):
    t0 = datetime(2019,06,11,1)+timedelta(hours=i)
    ax = geo_plots.add_map(bbox=(-98, -80,18.1, 30), bna=data_path+'BaseMaps/gulf.bna')
    geo_plots.plot_particles(ax,output_test,t0,marker='+',markersize=1)

#ax = geo_plots.add_vectors(ax,data_path+'Currents/hycom_forecast_20190611.nc',t0,2000,bbox=(-98, -88,18.1, 30), lonvar='lon',latvar='lat',uvar='u',vvar='v')
    plt.savefig('test'+str(i)+'.png')
