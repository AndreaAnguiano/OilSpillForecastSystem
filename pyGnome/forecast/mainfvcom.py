import os
from os.path import join
import time
import sys
from datetime import timedelta

def mainfvcom(position, namePosition, latbox, lonbox, start_time, duration, root_repo, forecast_path,
 data_path, daily_output_path, curr_path, wind_path, map_path,fvcom_fileName, depths, uvarfv, vvarfv,
 latvarfv, lonvarfv, depthvarfv, path2savefv, prefw, sufw, latvarw, lonvarw, uvarw, vvarw, path2savew, wpath, fvpath, grid_path):
    tic = time.clock()

    sys.path.append(forecast_path)
    sys.path.append(join(root_repo, 'pyGnome/pre_processing/'))
    #print join(root_repo, 'pyGnome/pre_processing/')
    import modelConfigF
    from fvcomforecast import fvcomforecast

# pre-proccesing currents and winds data
    yest = start_time - timedelta(days=1)
    tod_wrffile = prefw + str(start_time.year) + "-" + "{0:02d}".format(start_time.month)+ '-' + "{0:02d}".format(start_time.day)+ sufw
    tod_poswrffile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
    
    if os.path.exists(join(data_path, fvpath,fvcom_fileName)):
        fvcomforecast(start_time, start_time + duration, join(data_path, fvpath), fvcom_fileName, latbox, lonbox, depths, uvarfv, vvarfv, latvarfv, lonvarfv, depthvarfv, path2savefv, grid_path)
        currFile = 'fvcom_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
    else:
        'using old fvcom files'
        duration = duration - timedelta(days=1)
        currFile = 'fvcom_forecast_' + str(yest.year) + "{0:02d}".format(yest.month) + "{0:02d}".format(yest.day) + '.nc'
    print os.path.exists(join(data_path, wind_path, tod_poswrffile)),join(data_path, wind_path, tod_poswrffile), os.path.exists(join(data_path, wpath, tod_wrffile)), join(data_path, wpath, tod_wrffile)
    if os.path.exists(join(data_path, wind_path, tod_poswrffile)):
        windFile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'

    elif os.path.exists(join(data_path, wpath, tod_wrffile)) is False:
        print 'using old wrf files'
        windFile = 'WRF_forecast_'+str(start_time.year) + "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day-1)+'.nc'
        if duration > timedelta(days=3):
            duration = timedelta(days=3)

    # define map name
    map = 'sargazo.bna'
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
    uncertain = True

    tidalFile = 'qwqw'
    # # Elements
    num_elements = 10000
    save_nc = True

    # physical properties of water
    temp_water = 280
    dif_coef = 10000

    tic = time.clock()

    model = modelConfigF.make_modelF(timeStep, start_time, duration, weatheringSteps, map, uncertain,
                                     data_path, curr_path, wind_path, map_path, reFloatHalfLife, windFile,
                                     currFile, tidalFile, num_elements, depths, lat, lon, daily_output_path,
                                     wind_scale, save_nc, timestep_outputs, weatherers, td, dif_coef, temp_water)

    model.full_run()
    print 'Done!!'

    toc = time.clock()

    print(toc-tic)
