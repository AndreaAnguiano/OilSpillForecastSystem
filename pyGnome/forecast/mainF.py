import os
from datetime import datetime, timedelta
from gnome import basic_types, scripting, utilities
import numpy as np
from gnome.environment import Water
from os.path import join
import time
import sys
def main(position, namePosition, latbox, lonbox):
    tic = time.clock()

    root_repo= '/home/andrea/python/OilSpillForecastSystem/'#'/media/osz1/DATA/Dropbox/MyProjects/UNAM/OilSpill_Andrea/OilSpillForecastSystem/'
    forecast_folder= join(root_repo, 'pyGnome/forecast')
    data_folder= '/DATA/forecastData/'
    sys.path.append(forecast_folder)
    sys.path.append(join(root_repo,'pyGnome/pre_processing'))
    #spill timming
    now = datetime.now()
    start_time = datetime(now.year,now.month, now.day,1)-timedelta(days=1)
    duration = timedelta(days=4)
    # add paths
    today_folder = str(start_time.year)+ "{0:02d}".format(start_time.month)+ "{0:02d}".format(start_time.day)+'/'
    
    data_path = os.path.dirname(join(root_repo,'Data/'))
    daily_output_path =os.path.dirname(join(root_repo,'Output/', today_folder, namePosition+'/'))##,today_folder, namePosition+'/'))  #os.path.dirname(join(data_folder,'Outputs/', today_folder, namePosition+'/')
    print daily_output_path
    curr_path = 'Currents/'
    wind_path = 'Winds/'
    map_path = 'BaseMaps/'

    from modelConfigF import make_modelF
    from cutcoords import cutCoords
    from hycomforecast import hycomforecast
    from wrfforecast import wrfforecast
    from numb2month import numb2month
    #pre-proccesing currents and winds data
    prefhy = 'hycom_gomu_901m000_'
    sufhy = '_t000.nc'
    
     # depths
    depths = [0]

    #spill location
    lon = position[0]
    lat = position[1]
    print lat, lon 
    #netcdf's variables names 
    uvarhy = 'water_u'
    vvarhy = 'water_v'
    latvarhy = 'lat'
    lonvarhy = 'lon'
    depthvarhy = 'depth'
    
    path2savehy = join(data_path, curr_path)
    hycomforecast(start_time, start_time+timedelta(days=5),join(data_folder, 'hycom/') ,prefhy,sufhy,latbox,lonbox, depths, uvarhy,vvarhy, latvarhy,lonvarhy, depthvarhy, path2savehy)
    
    #pth = '/DATA/forecastData/wrf/04_abril/'
    prefw = 'wrfout_d01_'
    sufw= '_00.nc'
    latvarw = 'XLAT'
    lonvarw = 'XLONG'
    uvarw = 'U10'
    vvarw = 'V10'
    path2savew = join(data_path, wind_path)
    wpath = 'wrf/'+"{0:02d}".format(start_time.month)+'_'+numb2month(start_time.month)+'/'
    wrfforecast(start_time, start_time+timedelta(days=5), join(data_folder,wpath),prefw, sufw, latbox, lonbox, uvarw, vvarw, latvarw, lonvarw, path2savew)
    toc = time.clock()
    print(toc-tic)
    #define map name
    map = 'gulf.bna'
    reFloatHalfLife = -1 # Particles that beach on the shorelines are randomly refloated according to the specified half-life (specified in hours). 

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
    #=======
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
    model = make_modelF(timeStep,start_time, duration, weatheringSteps, map, uncertain, data_path,curr_path,wind_path,map_path, reFloatHalfLife, windFile, currFile, tidalFile,
               num_elements, depths, lat, lon, daily_output_path,wind_scale, save_nc, timestep_outputs, weatherers, td,dif_coef,temp_water)

    model.full_run()

        # for step in model:
            #print step
            # print "step: %.4i -- memuse: %fMB" % (step['step_num'],
         #                                       utilities.get_mem_use())
    print("Done!!!")
    toc = time.clock()
    print(toc-tic)
