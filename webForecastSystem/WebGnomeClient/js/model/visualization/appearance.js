//A model that stores appearance settings for various objects.

define([
    'underscore',
    'jquery',
    'backbone',
    'localforage',
], function(_, $, Backbone, localforage){
    'use strict';
    var appearanceModel = Backbone.Model.extend({
        appearance_cache : localforage.createInstance({name: 'Appearance Data Cache',
                                                    }),

        defaults: {
            on: false,
            ctrl_names: {title:'Object Appearance',
                         on: 'Show'},
            _type: 'appearance',
            id: 'default'
        },

        initialize: function(attrs, options) {
            Backbone.Model.prototype.initialize.call(this, attrs, options);
            if(options && options.default) {
                this.set(options.default, {silent:true});
                this.default = options.default;
            } else {
                this.default = {};
            }
            // if specified, it will fetch previously saved from cache. 
            if(options && options.cache) {
                this.fetch();
            }
            this.listenTo(this, 'change', this.save);
        },

        fetch: function(options) {
            return new Promise(_.bind(function(resolve, reject) {
                this.appearance_cache.getItem(this.get('id') + '_appearance').then(
                    _.bind(function(attrs) {
                        if (attrs) {
                            var keys = Object.keys(attrs);
                            for (var i = 0; i < keys.length; i++) {
                                if(this.has(keys[i]) && options && options.preserve){
                                    delete attrs[keys[i]];
                                }
                            }
                            this.set(attrs, {silent:true});
                            resolve(attrs);
                        } else {
                            resolve(attrs);
                        }
                    }, this)
                );
            }, this));
        },

        save: function(attrs, options) {
            if(this.get('id')) {
                this.appearance_cache.setItem(this.get('id') + '_appearance', this.toJSON());
            }
        },

        clearCache: function() {
            this.appearance_cache.removeItem(this.get('id') + '_appearance');
        },

        resetToDefault: function() {
            var id = this.id;
            this.clear();
            this.set(this.default,{silent: true});
            this.set({id:id},{silent: true});
            this.save();
        }

    });
    return appearanceModel;
});
