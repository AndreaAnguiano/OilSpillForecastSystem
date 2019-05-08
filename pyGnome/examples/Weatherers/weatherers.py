from gnome.utilities.remote_data import get_datafile
from gnome.model import Model
from gnome.map import GnomeMap
from gnome.map import MapFromBNA
from gnome.spill import point_line_release_spill
from gnome.movers import RandomMover, constant_wind_mover, GridCurrentMover, GridWindMover
from gnome.outputters import Renderer, NetCDFOutput
from gnome import scripting
import os
from gnome.basic_types import datetime_value_2d
from gnome.basic_types import numerical_methods
from gnome.environment import GridCurrent, constant_wind, Water, Waves
from gnome.outputters.animated_gif import Animation
from gnome.movers.py_current_movers import PyCurrentMover
from gnome.movers.py_wind_movers import PyWindMover
import os, numpy as np
from datetime import datetime, timedelta
from gnome.weatherers import Emulsification, Evaporation, NaturalDispersion, ChemicalDispersion, Burn, Skimmer, WeatheringData

def allWeatherers(timeStep, start_time, duration, weatheringSteps, map, uncertain, data_path, curr_path, wind_path, map_path, reFloatHalfLife, windFile, currFile, tidalFile, num_elements, depths, lat, lon, output_path, wind_scale, save_nc, timestep_outputs, weatherers, td):
    print 'initializing the model:'
    model = Model(time_step=timeStep, start_time=start_time, duration=duration)
    print 'adding the map:'
    map_folder = os.path.join(data_path, map_path)
    if not(os.path.exists(map_folder)):
        print('The map folder is incorrectly set:', map_folder)
    mapfile = get_datafile( os.path.join(map_folder,map) )

    model.map = MapFromBNA(mapfile, refloat_halflife=reFloatHalfLife)
    print 'adding a renderer'
    model.outputters += Renderer(mapfile, output_path, size=(800, 600), output_timestep=timedelta(hours=1))
    if save_nc:
        nc_outputter = NetCDFOutput(netcdf_file, which_data='most', output_timestep=timedelta(hours=1))
        model.outputters += nc_outputter
    print 'adding a wind mover:'
    wind_file = get_datafile(os.path.join(data_path, wind_path, windFile))
    wind = GridWindMover(wind_file)
    wind.wind_scale = wind_scale
    model.movers += wind
    print 'adding a current mover: '
    curr_file = get_datafile(os.path.join(data_path, curr_path, currFile))
    model.movers += GridCurrentMover(curr_file, num_method='RK4')
    if td:
        random_mover = RandomMover(diffusion_coef=10000)
        model.movers += random_mover
    print 'adding spill'
    model.spills += point_line_release_spill(num_elements=num_elements, start_position=(lon, lat, 0), release_time=start_time, end_release_time=start_time + duration)
    print 'adding weatherers'
    water = Water(280.92)
    wind = constant_wind(20.0, 117, 'knots')
    waves = Waves(wind, water)
    model.weatherers += Evaporation(water, wind)
    model.weatherers += Emulsification(waves)
    model.weatherers += NaturalDispersion(waves, water)
    return model

