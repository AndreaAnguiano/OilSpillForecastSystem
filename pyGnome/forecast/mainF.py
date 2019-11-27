import os
from datetime import timedelta
from os.path import join
import time
import sys


def main(position, namePosition, latbox, lonbox, start_time, duration, root_repo,
forecast_path, data_path, daily_output_path, curr_path, wind_path, map_path,
prefhy, sufhy, depths, uvarhy, vvarhy, latvarhy, lonvarhy, depthvarhy, path2savehy,
prefw, sufw, latvarw, lonvarw, uvarw, vvarw, path2savew, wpath):
    tic = time.clock()
    sys.path.append(forecast_path)
    sys.path.append(join(root_repo, 'pyGnome/pre_processing'))

    from modelConfigF import make_modelF
    from hycomforecast import hycomforecast
    from wrfforecast import wrfforecast
    # pre-proccesing currents and winds data
    yest = start_time - timedelta(days=1)
    tod_hycomfile = prefhy + str(start_time.year) + "{0:02d}".format(start_time.month) + "{0:02d}".format(start_time.day) + '12_t000.nc'
    tod_wrffile = prefw + str(start_time.year) + "-" + "{0:02d}".format(start_time.month) + '-'+ "{0:02d}".format(start_time.day) + sufw
    tod_poshycomfile = 'hycom_forecast_' + str(start_time.year) + "{0:02d}".format(start_time.month) + "{0:02d}".format(start_time.day) + '.nc'
    tod_poswrffile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month) + "{0:02d}".format(start_time.day) + '.nc'

    if os.path.exists(join(data_path, curr_path, tod_poshycomfile)):
        currFile = 'hycom_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month) + "{0:02d}".format(start_time.day) + '.nc'
    elif not os.path.exists(join(data_path, curr_path, tod_poshycomfile)) and not os.path.exists(join(data_path, 'hycom/', tod_hycomfile)):
        'using old hycom files'
        duration = duration - timedelta(days=1)
        currFile = 'hycom_forecast_'+str(yest.year) + "{0:02d}".format(yest.month) + "{0:02d}".format(yest.day) + '.nc'
    else:
        hycomforecast(start_time, start_time+timedelta(days=5), join(data_path, 'hycom/'), prefhy, sufhy, latbox, lonbox, depths, uvarhy, vvarhy, latvarhy, lonvarhy, depthvarhy, path2savehy)
        currFile = 'hycom_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month) + "{0:02d}".format(start_time.day) + '.nc'
    if os.path.exists(join(data_path, wind_path, tod_poswrffile)):
        windFile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month) + "{0:02d}".format(start_time.day) + '.nc'
    elif not os.path.exists(join(data_path, wpath, tod_wrffile)):
        print 'using old wrf files'
        windFile = 'WRF_forecast_'+str(yest.year) + "{0:02d}".format(yest.month) + "{0:02d}".format(yest.day) + '.nc'
        if duration > timedelta(days=3):
            duration = timedelta(days=3)
    else:
        wrfforecast(start_time, start_time+timedelta(days=5), join(data_path, wpath), prefw, sufw, latbox, lonbox, uvarw, vvarw, latvarw, lonvarw, path2savew)
        windFile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month) + "{0:02d}".format(start_time.day) + '.nc'

    # define map name
    map = 'gulf.bna'
    reFloatHalfLife = -1  # Particles that beach on the shorelines are randomly refloated according to the specified half-life (specified in hours).
    # spill location
    lon = position[0]
    lat = position[1]

    # timestep (s)
    timeStep = 3600
    # timestep for outputs
    timestep_outputs = 1

    # oil decay (weathering)
    weatherers = True
    weatheringSteps = 1  # how many weathering substeps to run inside a single model time step

    # turbulent diffusion
    td = True

    # wind scale
    wind_scale = 1

    # model uncertain
    uncertain = False

    tidalFile = 'qwqw'
    # # Elements
    num_elements = 10000
    save_nc = True

    # physical properties of water
    temp_water = 280
    dif_coef = 10000

    tic = time.clock()
    print duration
    model = make_modelF(timeStep, start_time, duration, weatheringSteps, map,
    uncertain, data_path, curr_path, wind_path, map_path, reFloatHalfLife,
    windFile, currFile, tidalFile, num_elements, depths, lat, lon, daily_output_path,
    wind_scale, save_nc, timestep_outputs, weatherers, td, dif_coef, temp_water)

    model.full_run()
    print 'Done!!'

    toc = time.clock()

    print(toc-tic)
