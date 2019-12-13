define([
    'underscore',
    'backbone',
    'model/base'
], function(_, Backbone, BaseModel){
    var windages = BaseModel.extend({
        urlRoot: '/initializers/',

        defaults: {
            'windage_range': [
                 0.01,
                 0.04
            ],
            'obj_type': 'gnome.spill.elements.InitWindages',
            'windage_persist': 900
        }
    });

    return windages;
});