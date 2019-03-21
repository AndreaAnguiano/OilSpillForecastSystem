import os
from datetime import datetime, timedelta
from gnome import basic_types, scripting, utilities
import numpy as np
from gnome.environment import Water

import time
tic = time.clock()
from modelConfig import *

import sys

sys.path.append('/home/andrea/python/OilSpillForecastSystem/pyGnome/examples/CurrentsAndWinds/')
sys.path.append('/home/andrea/python/OilSpillForecastSystem/pyGnome/examples/only_Winds/')
sys.path.append('/home/andrea/python/OilSpillForecastSystem/pyGnome/examples/only_Currents/')

sys.path.append('/home/andrea/python/OilSpillForecastSystem/pyGnome/examples/Weatherers/')

from CurrentsAndWinds import CurrentsAndWinds
from only_Winds import only_Winds
from only_Currents import only_Currents
from weatherers import allWeatherers
# add paths

data_path = os.path.dirname('/home/andrea/python/OilSpillForecastSystem/Data/')
output_path = os.path.dirname('/home/andrea/python/outputs/testweatherers/')
curr_path = 'Currents/'
wind_path = 'Winds/'
map_path = 'BaseMaps/'
#data_path = os.path.dirname('Data/')
#output_path = os.path.dirname('output/')

#define map name
map = 'gulf.bna'
reFloatHalfLife = -1 # Particles that beach on the shorelines are randomly refloated according to the specified half-life (specified in hours). 

# spill timming
start_time = datetime(2010,4,22)
duration = timedelta(days=10)

#timestep (s)
timeStep = 3600
#timestep for outputs
timestep_outputs = 1

#oil decay (weathering)
weatherers = True
weatheringSteps = 5 #how many weathering substeps to run inside a single model time step
evaporation = False

#turbulent diffusion
td = True

#wind scale
wind_scale = 1

#model uncertain
uncertain = False

#Files
#<<<<<<< HEAD
#windFile = 'WRF_20100422-20100731.nc'
#=======
windFile = 'WRF_v3_20100422-20100511.nc'
#>>>>>>> d3ff03e... data
#currFile = 'Synthetic/Currtest.nc'
currFile = 'hycom_v4_20100422-20100522.nc'

tidalFile = 'VDATUM_EC2001.nc'

# # Elements
num_elements = 28181

# depths
depths = [0]

#spill location
lat = 28.738
lon = -88.366

#saving options
save_nc = False

if __name__ == '__main__':
    scripting.make_images_dir()
    model = only_Currents(timeStep,start_time, duration, weatheringSteps, map, uncertain, data_path,curr_path,wind_path,map_path, reFloatHalfLife, windFile, currFile, tidalFile,
               num_elements, depths, lat, lon, output_path,wind_scale, save_nc, timestep_outputs, weatherers, td)

    model.full_run()
    # for step in model:
        #print step
        # print "step: %.4i -- memuse: %fMB" % (step['step_num'],
        #                                       utilities.get_mem_use())
    print("Done!!!")
toc = time.clock()
print(toc-tic)
