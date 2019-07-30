define([
    'underscore',
    'jquery',
    'backbone',
    'model/base',
    'moment',
    'localforage'
], function(_, $, Backbone, BaseModel, moment, localforage){
    'use strict';
    var baseEnvObj = BaseModel.extend({
        urlRoot: '/environment/',
        env_obj_cache : localforage.createInstance({name: 'Environment Object Data Cache',
                                                    }),

        initialize: function(attrs, options) {
            BaseModel.prototype.initialize.call(this, attrs, options);
            localforage.config({
                name: 'WebGNOME Cache',
                storeName: 'webgnome_cache'
            });
        },
    });

    return baseEnvObj;
});