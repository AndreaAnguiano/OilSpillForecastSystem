from gnome.utilities.remote_data import get_datafile
from gnome.model import Model
from gnome.map import MapFromBNA
from gnome.spill import point_line_release_spill
from gnome.movers import RandomMover, GridCurrentMover, GridWindMover
from gnome.outputters import NetCDFOutput
from gnome import scripting
import os
from gnome.environment import constant_wind, Water, Waves
from datetime import timedelta
from gnome.weatherers import Emulsification, Evaporation, NaturalDispersion, ChemicalDispersion


def make_modelF(timeStep, start_time, duration, weatheringSteps, map, uncertain, data_path, curr_path, wind_path, map_path, reFloatHalfLife, windFile, currFile, tidalFile, num_elements, depths, lat, lon, output_path, wind_scale, save_nc, timestep_outputs, weatherers, td, dif_coef,temp_water):
    print 'initializing the model:'
    model = Model(time_step=timeStep, start_time=start_time, duration=duration)
    print 'adding the map:'
    print os.path.join(data_path, map_path, map)
    mapfile = get_datafile(os.path.join(data_path, map_path, map))
    model.map = MapFromBNA(mapfile, refloat_halflife=reFloatHalfLife)
    print 'adding a renderer'

    if save_nc:
        scripting.remove_netcdf(output_path+'/'+'output.nc')
        nc_outputter = NetCDFOutput(output_path+'/'+'output.nc', which_data='standard', output_timestep=timedelta(hours=timestep_outputs))
        model.outputters += nc_outputter

    print 'adding a wind mover:'
    wind_file = get_datafile(os.path.join(data_path, wind_path, windFile))
    wind = GridWindMover(wind_file)
    # wind.wind_scale = wind_scale
    model.movers += wind
    print 'adding a current mover:'
    curr_file = get_datafile(os.path.join(data_path, curr_path, currFile))
    print curr_file
    model.movers += GridCurrentMover(curr_file, num_method='RK4')
    if td:
        random_mover = RandomMover(diffusion_coef=dif_coef)
        model.movers += random_mover
    print 'adding spill'
    model.spills += point_line_release_spill(num_elements=num_elements, start_position=(lon, lat, 0), release_time=start_time, end_release_time=start_time + duration)#, substance='AD04001', amount=9600000, units='kg')

    if weatherers:
        print 'adding weatherers'
        water = Water(temp_water)
        wind = constant_wind(0.0001, 0, 'knots')
        waves = Waves(wind, water)
        model.weatherers += Evaporation(water, wind)
    # model.weatherers += Emulsification(waves)
        model.weatherers += NaturalDispersion(waves, water)
    return model
