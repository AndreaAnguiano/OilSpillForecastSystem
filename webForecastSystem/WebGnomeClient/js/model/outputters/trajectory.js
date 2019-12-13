define([
    'underscore',
    'backbone',
    'model/base'
], function(_, Backbone, BaseModel){
    'use strict';
    var trajectoryOutputter = BaseModel.extend({
        urlRoot: '/outputter/',

        defaults: {
            'obj_type': 'gnome.outputters.geo_json.TrajectoryGeoJsonOutput',
            'output_timestep': null,
            'output_last_step': 'true',
            'output_zero_step': 'true',
            'name': 'TrajectoryGeoJsonOutput'
        },

        toTree: function(){
            return '';
        }
    });

    return trajectoryOutputter;
});