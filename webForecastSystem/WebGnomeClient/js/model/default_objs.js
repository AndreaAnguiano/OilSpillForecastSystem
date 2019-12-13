define([
    'underscore',
    'backbone',
    'model/base',
    'model/environment/waves'
], function(_, Backbone, BaseModel, WavesModel){
    'use strict';
    var defaultObjs = Backbone.Model.extend({
        /*
        Object that listens to the model and handles default references for
        environment objects. Also manages the Waves object for the Model
        */
        defaults: {
            'wind': null,
            'water': null,
            'waves': null,
            'windSpecified': false,
            'waterSpecified': false,
            'hasSubstance': false
        },

        initialize: function(options, model) {
            this.set(this.defaults);
            this.listenTo(model, 'fetched', this.fetchHandler);
            this.listenTo(model.get('environment'), 'add', this.addObj);
            this.listenTo(model.get('environment'), 'remove', this.removeObj);
            this.listenTo(model.get('spills'), 'change', this.checkSubstance);
            this.listenTo(model.get('spills'), 'add remove change', this.checkSubstance);
            this.listenTo(model.get('weatherers'), 'add', this.attachNewWeatherer);
            this.listenTo(this, 'new_wind new_water', this.manageWaves);
            this.listenTo(this, 'change', this.weatheringValid);
        },

        fetchHandler: function(model) {
            var env_objs = model.get('environment');
            var waves = env_objs.findWhere({'obj_type': 'gnome.environment.waves.Waves'});
            if (waves) {
                this.manageWaves(waves);
            } else {
                env_objs.map(_.bind(this.addObj,this));
            }
            
        },

        addObj: function(mod) {
            if (mod.get('obj_type').toLowerCase().includes('wind') &&
               this.get('wind') === null &&
               !this.get('windSpecified')) {
                this.set('wind', mod);
                this.trigger('new_wind', mod);
            }
            if (mod.get('obj_type').toLowerCase().includes('water') &&
               this.get('water') === null &&
               !this.get('waterSpecified')) {
                this.set('water', mod);
                this.trigger('new_water', mod);
            }
        },

        removeObj: function(mod) {
            if (mod === this.get('wind')){
                this.set('wind', null);
                this.set('windSpecified', false);
                this.trigger('new_wind', null);
            }
            if (mod === this.get('water')){
                this.set('water', null);
                this.set('waterSpecified', false);
                this.trigger('new_water', null);
            }
        },

        manageWaves: function(mod) {
            if (mod === null && this.get('waves') !== null) {
                webgnome.model.get('environment').remove(this.get('waves'));
                this.set('waves', null);
                this.trigger('new_waves', null);
            } else if (this.get('wind') && this.get('water') && this.get('waves') === null) {
                var waves = new WavesModel();
                waves.set('wind', this.get('wind'));
                waves.set('water', this.get('water'));
                waves.save(null, {
                    validate: false,
                    success: _.bind(function(mod){
                        webgnome.model.get('environment').add(mod);
                        webgnome.model.save();
                        this.set('waves', mod);
                    }, this)
                });
            } else if (mod !== null && mod.get('obj_type').toLowerCase().includes('waves')) {
                //pass waves object directly
                this.set('waves', mod);
                if(!this.get('wind')) {
                    this.set('wind', mod.get('wind'));
                }
                if(!this.get('wind')) {
                    this.set('water', mod.get('water'));
                }
                if (!webgnome.model.get('environment').contains(mod)) {
                    webgnome.model.get('environment').add(mod);
                }
            }
        },

        checkSubstance: function() {
            var hasSubstance = false;
            var spills = webgnome.model.get('spills');
            if (spills.length > 0) {
                var element_type = spills.at(0).get('element_type');
                if (element_type && element_type.get('substance') !== null) {
                    hasSubstance = true;
                }
            }
            this.set('hasSubstance', hasSubstance);
        },

        attachNewWeatherer: function(weatherer) {
            if (this.get('waves') != null && _.isNull(weatherer.get('waves'))) {
                weatherer.set('waves', this.get('waves'));
            }
            if (this.get('water') != null && _.isNull(weatherer.get('water'))) {
                weatherer.set('water', this.get('water'));
            }
            if (this.get('wind') != null && _.isNull(weatherer.get('wind'))) {
                weatherer.set('wind', this.get('wind'));
            }
            weatherer.save();
        },

        weatheringValid: function() {
            if (this.get('hasSubstance') &&
                !_.isUndefined(this.get('waves')) &&
                !_.isUndefined(this.get('water')) &&
                !_.isUndefined(this.get('wind'))) {
                this.trigger('weatheringOn');
            } else {
                this.trigger('weatheringOff');
            }
        }

    });
    return defaultObjs;
});