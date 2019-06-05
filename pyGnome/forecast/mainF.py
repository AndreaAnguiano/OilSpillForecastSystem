import os
from datetime import datetime, timedelta
from gnome import basic_types, scripting, utilities
import numpy as np
from gnome.environment import Water
from os.path import join
import time
import sys
def main(position, namePosition, latbox, lonbox, start_time, duration, root_repo, forecast_path, data_path, daily_output_path, curr_path,wind_path, map_path, prefhy, sufhy,depths, uvarhy,vvarhy,latvarhy,lonvarhy,depthvarhy, path2savehy,prefw, sufw,latvarw,lonvaw,uvarw,vvarw,path2savew):
    tic = time.clock()  
    sys.path.append(forecast_path)
    sys.path.append(join(root_repo,'pyGnome/pre_processing'))

    from modelConfigF import make_modelF
    from cutcoords import cutCoords
    from hycomforecast import hycomforecast
    from wrfforecast import wrfforecast
    from numb2month import numb2month
    
    #pre-proccesing currents and winds data
    hycomforecast(start_time, start_time+timedelta(days=5),join(data_path, 'hycom/') ,prefhy,sufhy,latbox,lonbox, depths, uvarhy,vvarhy, latvarhy,lonvarhy, depthvarhy, path2savehy)
    
    wrfforecast(start_time, start_time+timedelta(days=5), join(data_path,wpath),prefw, sufw, latbox, lonbox, uvarw, vvarw, latvarw, lonvarw, path2savew)
    #define map name
    map = 'gulf.bna'
    reFloatHalfLife = -1 # Particles that beach on the shorelines are randomly refloated according to the specified half-life (specified in hours). 
    #spill location
    lon = position[0]
    lat = position[1]

    #timestep (s)
    timeStep = 3600
    #timestep for outputs
    timestep_outputs = 1

    #oil decay (weathering)
    weatherers = True
    weatheringSteps = 1 #how many weathering substeps to run inside a single model time step
    evaporation = True

    #turbulent diffusion
    td = True

    #wind scale
    wind_scale = 1

    #model uncertain
    uncertain = False

    #Files
    windFile = 'WRF_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
    currFile = 'hycom_forecast_'+str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'.nc'
    tidalFile = 'qwqw'
    # # Elements
    num_elements = 10000
    save_nc = True

    #physical properties of water
    temp_water = 280
    dif_coef = 10000
    
    tic = time.clock()
    
    model = make_modelF(timeStep,start_time, duration, weatheringSteps, map, uncertain, data_folder,curr_path,wind_path,map_path, reFloatHalfLife, windFile, currFile, tidalFile,
               num_elements, depths, lat, lon, daily_output_path,wind_scale, save_nc, timestep_outputs, weatherers, td,dif_coef,temp_water)

    model.full_run()
    print 'Done!!'
    
    toc = time.clock()
    
    print(toc-tic)
