import os
from datetime import datetime, timedelta
from gnome import basic_types, scripting, utilities
import numpy as np
from gnome.environment import Water

import time
tic = time.clock()
from modelConfig import *
# add paths

data_path = os.path.dirname('/home/andrea/python/OilSpillForecastSystem/Data/')
output_path = os.path.dirname('/home/andrea/python/OilSpillForecastSystem/outputs/testanothwindscale/')

#data_path = os.path.dirname('Data/')
#output_path = os.path.dirname('output/')

#define map name
map = 'gulf.bna'
reFloatHalfLife = -1 # Particles that beach on the shorelines are randomly refloated according to the specified half-life (specified in hours). # If no refloating is desired set this value to -1.

# spill timming
startDate = datetime(2010,04,22)
duration = timedelta(days=10)


#timestep (s)
timeStep = 3600

#oil decay (weathering)
weatheringSteps = 5 #how many weathering substeps to run inside a single model time step
evaporation = False

#model uncertain
uncertain = False

#Files
windFile = 'WRF_20100422-20100731.nc'
#currFile = 'Synthetic/Currtest.nc'
currFile = 'hycom_v4_20100422-20100731.nc'

tidalFile = 'VDATUM_EC2001.nc'

# # Elements
num_elements = 28181

# depths
depths = [0]

#spill location
lat = 28.738
lon = -88.366
if __name__ == '__main__':
    scripting.make_images_dir()
    model = make_model(timeStep,startDate, duration, weatheringSteps, map, uncertain, data_path, reFloatHalfLife, windFile,
                       currFile, tidalFile, num_elements, depths, lat, lon, output_path,evaporation)

    model.full_run()
    # for step in model:
        #print step
        # print "step: %.4i -- memuse: %fMB" % (step['step_num'],
        #                                       utilities.get_mem_use())
    print("Done!!!")
toc = time.clock()
print(toc-tic)
