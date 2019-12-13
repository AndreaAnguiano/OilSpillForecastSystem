define([
    'underscore',
    'backbone',
    'model/movers/base'
], function(_, Backbone, BaseMover){
    'use strict';
    var iceMover = BaseMover.extend({
        defaults: {
            obj_type: 'gnome.movers.current_movers.IceMover'
        },

        toTree: function(){
            return '';
        }
    });

    return iceMover;
});