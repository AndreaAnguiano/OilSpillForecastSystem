from gnome.utilities.remote_data import get_datafile
from gnome.model import Model
from gnome.map import GnomeMap
from gnome.map import MapFromBNA
from gnome.spill import point_line_release_spill
from gnome.movers import RandomMover, constant_wind_mover, GridCurrentMover, GridWindMover
from gnome.outputters import Renderer, NetCDFOutput
from gnome.environment import Water
from gnome.weatherers import Evaporation
from gnome.environment.wind import constant_wind
from gnome import scripting
import os
from gnome.basic_types import datetime_value_2d
from gnome.basic_types import numerical_methods
from gnome.environment import GridCurrent
from gnome.outputters.animated_gif import Animation
from gnome.movers.py_current_movers import PyCurrentMover
from gnome.movers.py_wind_movers import PyWindMover
import os
import numpy as np
from datetime import datetime, timedelta

def make_model(timeStep,start_time, duration, weatheringSteps, map, uncertain, data_path, reFloatHalfLife, windFile, currFile, tidalFile,
               num_elements, depths, lat, lon, output_path, evaporation):
    #initalizing the model
    print 'initializing the model:'
    # model = Model(time_step = timeStep, start_time= start_time, duration=duration, uncertain = uncertain)
    model = Model(time_step = timeStep, start_time= start_time, duration=duration)

    #adding the map
    print 'adding the map:'

    mapfile = get_datafile(os.path.join(data_path, map))
    model.map = MapFromBNA(mapfile, refloat_halflife = reFloatHalfLife)
    #model.map = GnomeMap()


    print 'adding a renderer'
    # renderer is a class that writes map images for GNOME results
    model.outputters += Renderer(mapfile, output_path, size=(800, 600), output_timestep=timedelta(hours=1))
    ##scripting.remove_netcdf(netcdf_file)
    #nc_outputter = NetCDFOutput(netcdf_file, which_data='most', output_timestep=timedelta(hours=1))
    #model.outputters += nc_outputter
    #adding the movers

    print 'adding a wind mover:'
    wind_file = get_datafile(os.path.join(data_path, windFile))
    wind = GridWindMover(wind_file)
    wind.wind_scale = 2
    model.movers += wind

    print 'adding a current mover: '
    curr_file = get_datafile(os.path.join(data_path,currFile))
    model.movers+= GridCurrentMover(curr_file, num_method='RK4')
    #random_mover = RandomMover(diffusion_coef=10000) #in cm/sdfd
    #model.movers += random_mover

    if evaporation:
    
     #wind for evaporation
	print'adding evaporation'
    	wind = constant_wind(1, 0, 'knots')
    	water = Water(temperature=300.0, salinity=35.0)
    	model.weatherers += Evaporation(wind=wind, water=water)
    #

    print 'adding a spill'
    # for i in depths:
    #     model.spills+= point_line_release_spill(num_elements=num_elements, start_position=(lon,lat,i), release_time=start_time)
    model.spills+= point_line_release_spill(num_elements=num_elements, start_position=(lon,lat,0), release_time=start_time,
                                            end_release_time=start_time+timedelta(days=93))

    return model
