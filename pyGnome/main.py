import os
from datetime import datetime, timedelta
from gnome import basic_types, scripting, utilities
import numpy as np
from gnome.environment import Water
from os.path import join

import time
tic = time.clock()
from modelConfig import *

import sys

#root_repo='/media/osz1/DATA/Dropbox/MyProjects/UNAM/OilSpill_Andrea/OilSpillForecastSystem/'
root_repo='/home/andrea/python/OilSpillForecastSystem/'
examples_folder=join(root_repo,'pyGnome/examples')

sys.path.append(join(examples_folder,'CurrentsAndWinds'))
sys.path.append(join(examples_folder,'only_Winds'))
sys.path.append(join(examples_folder,'only_Currents'))
sys.path.append(join(examples_folder,'Weatherers'))

from CurrentsAndWinds import CurrentsAndWinds
from only_Winds import only_Winds
from only_Currents import only_Currents
from weatherers import allWeatherers
# add paths

data_path = os.path.dirname(join(root_repo,'Data/'))
output_path = os.path.dirname(join(root_repo,'Output/'))
curr_path = 'Currents/'
wind_path = 'Winds/'
map_path = 'BaseMaps/'
#adding the physical process choosed. 'Currents' for only currents, 'Winds' for only winds, 'CurrentsAndWinds' for currents and winds and 'Weatherers' for weatherers.  
phys_example = 'Weatherers'

#define map_file name
map_file = 'gulf.bna'
reFloatHalfLife = -1 # Particles that beach on the shorelines are randomly refloated according to the specified half-life (specified in hours). 

# spill timmin
start_time = datetime(2010,4,22)
duration = timedelta(days=10)

#timestep (s)
timeStep = 3600
#timestep for outputs
timestep_outputs = 1

#oil decay (weathering)
weatherers = False
weatheringSteps = 5 #how many weathering substeps to run inside a single model time step
evaporation = False

#turbulent diffusion
td = True

#wind scale
wind_scale = 1

#model uncertain
uncertain = False

#Files
windFile = 'WRF_v3_20100422-20100511.nc'
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
    if phys_example == 'CurrentsAndWinds':
        model = CurrentsAndWinds(timeStep,start_time, duration, weatheringSteps, map_file, uncertain, data_path,curr_path,wind_path,map_path, reFloatHalfLife, windFile, currFile, tidalFile,num_elements, depths, lat, lon, output_path,wind_scale, save_nc, timestep_outputs, weatherers, td)
    if phys_example == 'Currents':
        model = only_Currents(timeStep,start_time, duration, weatheringSteps, map_file, uncertain, data_path,curr_path,wind_path,map_path, reFloatHalfLife, windFile, currFile, tidalFile,num_elements, depths, lat, lon, output_path,wind_scale, save_nc, timestep_outputs, weatherers, td)
    if phys_example == 'Winds':
        model = only_Winds(timeStep,start_time, duration, weatheringSteps, map_file, uncertain, data_path,curr_path,wind_path,map_path, reFloatHalfLife, windFile, currFile, tidalFile,num_elements, depths, lat, lon, output_path,wind_scale, save_nc, timestep_outputs, weatherers, td)
    if phys_example == 'Weatherers':
        model = allWeatherers(timeStep,start_time, duration, weatheringSteps, map_file, uncertain, data_path,curr_path,wind_path,map_path, reFloatHalfLife, windFile, currFile, tidalFile,num_elements, depths, lat, lon, output_path,wind_scale, save_nc, timestep_outputs, weatherers, td)

    model.full_run()
    print("Done!!!")
toc = time.clock()
print(toc-tic)
