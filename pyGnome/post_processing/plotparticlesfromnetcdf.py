from post_gnome.plotting import geo_plots
reload(geo_plots)
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from post_gnome import nc_particles
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
from post_gnome import nc_particles
from netCDF4 import Dataset, num2date
import numpy as np


plt.clf()
lat = [18.1, 30]
lon = [-98, -88]
ax = geo_plots.add_map(bbox=(-98, -88,18.1, 30), bna='/DATA/forecastData/BaseMaps/gulf.bna')
#if bbox not specified, this will use map bounds from bna

def contour_particles(ax, filename, t, depth=0, varname=None, criteria=None, levels=[0.1, 0.4, 0.8, 1]):
    '''
    contour all LEs at one time step
    ax: (matplotlib.axes object) the map on which the LEs will be plotted
    filename: (str) complete path filename of particle file
    t: (datetime obj) closest time to this will be plottted
    depth: (float) depth of particles to include (all if None)
    '''
    import scipy.stats as st
    particles = nc_particles.Reader(filename)
    times = particles.times
    dt = [np.abs(((output_t - t).total_seconds()) / 3600) for output_t in times]
    tidx = dt.index(min(dt))
    if varname is not None:
        variables = ['latitude', 'longitude', 'status_codes', 'depth'] + [varname]
    try:
        TheData = particles.get_timestep(tidx, variables=variables)
    except:  # GUI GNOME < 1.3.10
        TheData = particles.get_timestep(tidx, variables=['latitude', 'longitude', 'status_codes', 'depth'])
        #TheData['status_codes'] = TheData['status_co']
    if varname is None or criteria is None:
        pid = np.where((TheData['status_codes'] == 2) & (TheData['depth'] == depth))[0]
    else:
        print 'Applying criteria'
        print TheData[varname].min(), TheData[varname].max()
        pid = np.where((TheData['status_codes'] == 2) & (TheData['depth'] == depth) & (TheData[varname] < criteria))[0]
        print len(pid)

    x = TheData['longitude'][pid]
    y = TheData['latitude'][pid]

    # Peform the kernel density estimate
    xx, yy = np.mgrid[min(x) - .1:max(x) + .1:100j, min(y) - .1:max(y) + .1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)
    max_density = f.max()

    levels.sort()
    particle_contours = [lev * max_density for lev in levels]

    ax.contourf(xx, yy, f, particle_contours, transform=ccrs.PlateCarree())
    # ax.pcolor(xx,yy,f,transform=ccrs.PlateCarree())
    print 'Closest time found: ', times[tidx]

    return ax
contour_particles(ax,'../outputs/testtime/test_output.nc',datetime(2019,07,24),depth=0,varname=None,criteria=None,levels=[0.1, 0.4, 0.8, 1])
#geo_plots.plot_all_trajectories(ax,'../outputs/testtime/test_output.nc',addmarker=True)
#geo_plots.plot_single_trajectory(ax,'../outputs/testtime/test_output.nc',1,color='r')

plt.show()
