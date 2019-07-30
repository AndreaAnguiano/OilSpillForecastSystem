define([
    'jquery',
    'underscore',
    'backbone',
    'moment',
    'sweetalert',
    'model/base',
    'model/cache',
    'model/map/map',
    'model/map/param',
    'model/map/bna',
    'model/spill',
    'model/environment/tide',
    'model/environment/wind',
    'model/environment/water',
    'model/environment/waves',
    'model/environment/gridcurrent',
    'model/environment/gridwind',
    'model/movers/random',
    'model/movers/wind',
    'model/movers/py_wind',
    'model/movers/cats',
    'model/movers/grid_current',
    'model/movers/py_current',
    'model/movers/current_cycle',
    'model/movers/ice',
    'model/movers/component',
    'model/outputters/trajectory',
    'model/outputters/spill',
    'model/outputters/weathering',
    'model/outputters/current',
    'model/outputters/ice_raw',
    'model/outputters/ice_image',
    'model/outputters/netcdf',
    'model/outputters/kmz',
    'model/outputters/shape',
    'model/weatherers/evaporation',
    'model/weatherers/dispersion',
    'model/weatherers/natural_dispersion',
    'model/weatherers/emulsification',
    'model/weatherers/dissolution',
    'model/weatherers/fay_gravity_viscous',
    'model/weatherers/langmuir',
    'model/weatherers/weathering_data',
    'model/weatherers/burn',
    'model/weatherers/skim',
    'model/weatherers/manual_beaching',
    'model/weatherers/roc_skim',
    'model/weatherers/roc_burn',
    'model/weatherers/roc_disperse',
    'model/user_prefs',
    'model/risk/risk',
    'collection/movers',
    'collection/spills',
    'model/default_objs'
], function($, _, Backbone, moment, swal,
    BaseModel, Cache,
    MapModel, ParamMapModel, MapBnaModel, SpillModel,
    TideModel, WindModel, WaterModel, WavesModel, GridCurrentModel, GridWindModel,
    RandomMover, WindMover, PyWindMover,
    CatsMover, GridCurrentMover, PyCurrentMover, CurrentCycleMover,
    IceMover, ComponentMover,
    TrajectoryOutputter, SpillOutputter, WeatheringOutputter,
    CurrentOutputter, IceOutputter, IceImageOutputter,
    NetCDFOutputter, KMZOutputter, ShapeOutputter,
    EvaporationWeatherer, DispersionWeatherer, NaturalDispersionWeatherer,
    EmulsificationWeatherer, DissolutionWeatherer,
    FayGravityViscous, Langmuir, WeatheringData,
    BurnWeatherer, SkimWeatherer, BeachingWeatherer,
    RocSkimResponse, RocBurnResponse, RocDisperseResponse,
    UserPrefs, RiskModel, MoversCollection, SpillsCollection, DefaultObjs) {
    'use strict';
    var gnomeModel = BaseModel.extend({
        url: '/model',
        ajax: [],
        ref_hash: {},
        nonStandardOutputters: [
            'gnome.outputters.netcdf.NetCDFOutput',
            'gnome.outputters.shape.ShapeOutput',
            'gnome.outputters.kmz.KMZOutput',
            'gnome.outputters.image.IceImageOutput',
            'gnome.outputters.geo_json.TrajectoryGeoJsonOutput'
        ],
        model: {
            spills: {
                'gnome.spill.spill.Spill': SpillModel
            },
            map: {
                'gnome.map.GnomeMap': MapModel,
                'gnome.map.ParamMap': ParamMapModel,
                'gnome.map.MapFromBNA': MapBnaModel
            },
            environment: {
                'gnome.environment.wind.Wind': WindModel,
                'gnome.environment.tide.Tide': TideModel,
                'gnome.environment.water.Water': WaterModel,
                'gnome.environment.waves.Waves': WavesModel,
                'gnome.environment.environment_objects.GridCurrent': GridCurrentModel,
                'gnome.environment.environment_objects.GridWind': GridWindModel,
            },
            movers: {
                'gnome.movers.wind_movers.WindMover': WindMover,
                'gnome.movers.random_movers.RandomMover': RandomMover,
                'gnome.movers.current_movers.CatsMover': CatsMover,
                'gnome.movers.current_movers.IceMover': IceMover,
                'gnome.movers.current_movers.GridCurrentMover': GridCurrentMover,
                'gnome.movers.py_current_movers.PyCurrentMover': PyCurrentMover,
                'gnome.movers.py_wind_movers.PyWindMover': PyWindMover,
                'gnome.movers.current_movers.CurrentCycleMover': CurrentCycleMover,
                'gnome.movers.current_movers.ComponentMover': ComponentMover
            },
            outputters: {
                'gnome.outputters.geo_json.TrajectoryGeoJsonOutput': TrajectoryOutputter,
                'gnome.outputters.json.SpillJsonOutput': SpillOutputter,
                'gnome.outputters.weathering.WeatheringOutput': WeatheringOutputter,
                'gnome.outputters.json.CurrentJsonOutput': CurrentOutputter,
                'gnome.outputters.json.IceJsonOutput': IceOutputter,
                'gnome.outputters.image.IceImageOutput': IceImageOutputter,
                'gnome.outputters.kmz.KMZOutput': KMZOutputter,
                'gnome.outputters.netcdf.NetCDFOutput': NetCDFOutputter,
                'gnome.outputters.shape.ShapeOutput': ShapeOutputter
            },
            weatherers: {
                'gnome.weatherers.evaporation.Evaporation': EvaporationWeatherer,
                'gnome.weatherers.cleanup.ChemicalDispersion': DispersionWeatherer,
                'gnome.weatherers.emulsification.Emulsification': EmulsificationWeatherer,
                'gnome.weatherers.cleanup.Burn': BurnWeatherer,
                'gnome.weatherers.cleanup.Skimmer': SkimWeatherer,
                'gnome.weatherers.natural_dispersion.NaturalDispersion': NaturalDispersionWeatherer,
                'gnome.weatherers.manual_beaching.Beaching': BeachingWeatherer,
                'gnome.weatherers.spreading.FayGravityViscous': FayGravityViscous,
                'gnome.weatherers.spreading.Langmuir': Langmuir,
                'gnome.weatherers.weathering_data.WeatheringData': WeatheringData,
                'gnome.weatherers.dissolution.Dissolution': DissolutionWeatherer,
                'gnome.weatherers.roc.Skim': RocSkimResponse,
                'gnome.weatherers.roc.Burn': RocBurnResponse,
                'gnome.weatherers.roc.Disperse': RocDisperseResponse
            }
        },

        defaults: function(){
            return {
                obj_type: 'gnome.model.Model',
                time_step: 900,
                start_time: moment().add(1, 'hour').format('YYYY-MM-DDTHH:00:00'),
                duration: 86400,
                map: new MapModel(),
                outputters: new Backbone.Collection([
                    new SpillOutputter(),
                    new WeatheringOutputter(),
                    new CurrentOutputter(),
                    new IceOutputter()
                ]),
                weatherers: new Backbone.Collection([
                    new EvaporationWeatherer({on: false}),
                    new NaturalDispersionWeatherer({on: false}),
                    new EmulsificationWeatherer({on: false}),
                    new FayGravityViscous({on: false}),
                    new Langmuir({on: false}),
                    //new DissolutionWeatherer({on: false})
                ]),
                movers: new MoversCollection(),
                environment: new Backbone.Collection(),
                spills: new SpillsCollection()
            };
        },

        initialize: function(options){
            BaseModel.prototype.initialize.call(this, options);
            this.default_env_refs = new DefaultObjs(null, this);
            webgnome.user_prefs = new UserPrefs();
            webgnome.obj_ref = {};
            this.addListeners();
            for (var i = 0 ; i < this.get('weatherers').models.length; i++) {
                this.get('weatherers').models[i].addListeners(this);
            }
        },

        addListeners: function(){
            this.get('environment').on('change add remove', this.environmentChange, this);
            this.get('environment').on('add remove sort', this.configureMetaEnvironmentObjects, this);
            //this.get('environment').on('add remove sort', this.configureWindRelations, this);
            //this.get('environment').on('add remove sort', this.configureWaterRelations, this);
//            this.listenTo(this.get('environment'), 'remove', this.removeEnvObject)
            this.get('movers').on('change add remove', this.moversChange, this);
            this.get('movers').on('add', this.manageTides, this);
            this.get('spills').on('change add remove', this.spillsChange, this);
            this.get('spills').on('sync', this.spillsTimeComplianceWarning, this);
            this.on('change:start_time', this.spillsTimeComplianceCheck, this);
            this.on('change:start_time', this.adiosSpillTimeFix, this);
//            this.get('weatherers').on('change add remove', this.weatherersChange, this);
            this.get('outputters').on('change add remove', this.outputtersChange, this);
            this.get('movers').on('sync add save', this.moversTimeComplianceWarning, this);
            this.on('change:start_time', this.moversTimeComplianceCheck, this);
            this.on('change:map', this.validateSpills, this);
            this.on('change:map', this.addMapListeners, this);
            this.on('sync', webgnome.cache.rewind, webgnome.cache);
        },
/*
        removeEnvObject: function(model) {
            console.log(model);
            this.get('weatherers').forEach(function(w))
        },
*/
        addMapListeners: function(){
            this.get('map').on('change', this.mapChange, this);
        },

        mapChange: function(child){
            this.validateSpills(child);
            this.childChange('map', child);
        },

        environmentChange: function(child){
            this.childChange('environment', child);
        },

        moversChange: function(child){
            this.childChange('movers', child);
        },

        spillsChange: function(child){
            this.childChange('spills', child);
            if(this.get('uncertain')) {
                this.set('uncertain', false);
                this.save(null, {
                    success: _.bind(function(){
                        this.set('uncertain', true);
                        this.save();
                    }, this)});
            }
        },

        adiosSpillTimeFix: function() {
            if (this.get('mode') === 'adios') {
                var start_time = this.get('start_time');
                this.get('spills').each(function(model){
                    model.get('release').durationShift(start_time);
                });
            }
        },

        setupTides: function() {
            var movers = this.get('movers');
            var tides = [];

            movers.each(function(mover) {
                if (!_.isUndefined(mover.get('tide'))) {
                    tides.push(mover.get('tide'));
                }
            });

            this.get('environment').add(tides);
        },

        manageTides: function(model) {
            if (model.get('obj_type') === 'gnome.movers.current_movers.CatsMover') {
                if (!_.isUndefined(model.get('tide'))) {
                    this.get('environment').add(model.get('tide'));
                }
            }
        },

        spillsTimeComplianceCheck: function(model) {
            model.get('spills').forEach(function(spill) {
                var name = spill.get('name');
                var msg = spill.isTimeValid();
                // Add this info to logger?
                // The check just changes time_compliance attribute
            });
        },

        spillsTimeComplianceWarning: function(model) {
            var msg = model.isTimeValid();

            if (msg !== '') {
                swal({
                    title: msg,
                    text: "Would you like to change the model start time to match the spill's start time?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonText: "Yes",
                    cancelButtonText: "No"
                }).then(_.bind(function(correct) {
                    if (correct) {
                        var spillStart = model.get('release').get('release_time');
                        this.set('start_time', spillStart);
                        this.save();
                    }
                }, this));
            }
        },

        moversTimeComplianceCheck: function(model) {
            model.get('movers').forEach(function(mover) {
                var name = mover.get('name');
                var msg = mover.isTimeValid();
                //add this info to logger? the check just changes time_compliance attribute
            });
        },

        moversTimeComplianceWarning: function(model) {
            // model.save(null, {
            // validate: false,
            // success: _.bind(function(model) {
                // }, this)
            // });

            var msg = model.isTimeValid();
            if ( msg !== '') {
                swal({
                    title: 'Error',
                    text: msg,
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Fix',
                    cancelButtonText: 'Ignore'
                }).then(_.bind(function(options) {
                    if (options) {
                        swal({
                            title: 'Select a correction option:',
                            text: '<ul style="text-align:left"><li>Extrapolate the data (this option will extrapolate at both the beginning and end of the time series as necesssary)</li><li>Change the model start time to match the data (if you have set any spills, these start times may also need to be changed)</li></ul>',
                            type: 'warning',
                            showCancelButton: true,
                            confirmButtonText: 'Change Model Start',
                            cancelButtonText: 'Extrapolate Data'
                        }).then(_.bind(function(fit) {
                            if (fit) {
                                this.fitToInterval(model.dataActiveTimeRange()[0]);
                            }
                            else {
                                model.setExtrapolation(true);
                            }

                            model.set('time_compliance','valid');
                        }, this));
                    }
                }, this));
            }
        },

        outputtersChange: function(child){
            this.childChange('outputters', child);
        },

        validateSpills: function() {
            var spills = this.get('spills');
            var spillNames = '';
            for (var i = 0; i < spills.length; i++){
                if (!spills.at(i).isValid()){
                    spillNames += spills.at(i).get('name') + ' ';
                }
            }
            return spillNames;
        },

        validate: function(attrs, options) {
            // if(attrs.duration <= 0 || isNaN(attrs.duration)){
            //     return 'Duration values should be numbers only and greater than 0.';
            // }

            if (attrs.name === '') {
                return 'Model name must be entered.';
            }

            if(attrs.duration <= 0){
                return 'Duration values should be positive values.';
            }

            if(isNaN(attrs.duration)){
                return 'Duration values should be numbers only.';
            }

            if (!isNaN(attrs.time_step)){

                if(attrs.time_step <= 0){
                    return 'Time step must be a positive number.';
                }
            }
            else {
                return 'Time step values should be numbers only.';
            }

            if (this.validateSpills() !== ''){
                return this.validateSpills();
            }


            // if (attrs.map_id === null) {
            //     return 'Model requires a map.';
            // }

            // if (attrs.movers === null) {
            //     return 'Model doesn\'t have any movers.';
            // }

            // if (attrs.spills === null) {
            //     return 'Model requires at least one spill.';
            // }

            // if (attrs.environment === null) {
            //     return 'Model doesn\'t have an environment.';
            // }

            // if (attrs.start_time === null || attrs.duration) {
            //     return 'Model needs both start time and duration.';
            // }
        },

        composeInvalidMsg: function(arr) {
            var msg = '<code>';

            _.each(arr, function(el, i, list){
                msg += el.model.get('name') + ' <i>off by ' + el.timeDiff + '</i><br>';
            });

            msg += '</code>';

            return msg;
        },

        fitToInterval: function(start_time) {
            this.set('start_time', webgnome.secondsToTimeString(start_time));
            this.save();
        },



        formatDuration: function() {
            var duration = this.get('duration');

            var hours = duration / 3600;
            var days = hours / 24;

            if (Math.round(days) !== days) {
                if (days < 1){
                    days = 0;
                } else {
                    days = parseInt(days, 10);
                    hours = hours - (days * 24);
                }
            } else {
                hours = 0;
            }
            return {days: days, hours: hours};
        },

        activeTimeRange: function() {
            var start = webgnome.timeStringToSeconds(this.get('start_time'));
            var end = start + this.get('duration');

            return [start, end];
        },

        getEndTime: function() {
            var durationObj = this.formatDuration();
            var timeInHours = durationObj.days * 24 + durationObj.hours;
            var start_time = this.get('start_time');

            return moment(start_time).add(timeInHours, 'h').format('YYYY-MM-DDTHH:00:00');
        },

        durationString: function(start_str) {
            var str = start_str;
            var durationObj = this.formatDuration();
            var day_human = moment.duration(durationObj.days, 'days').humanize();
            var hour_human = moment.duration(durationObj.hours, 'hours').humanize();

            if (durationObj.days && durationObj.hours) {
                str += day_human + " and " + hour_human;
            }
            else if (durationObj.days) {
                str += day_human;
            }
            else if (durationObj.hours) {
                str += hour_human;
            }

            return str;
        },

        toTree: function(){
            var tree = {};
            var millisecsDur = this.get('duration') * 1000;
            var millisecsTime = this.get('time_step') * 1000;
            var duration = moment.duration(millisecsDur).asHours();
            var timeStepTime = moment.duration(millisecsTime).asMinutes();
            var map = this.get('map');
            var movers = this.get('movers');
            var environment = this.get('environment');
            var weatherers = this.get('weatherers');
            var spills = this.get('spills');
            var attrs = [];
            var startTime = moment(this.get('start_time')).format('lll');

            timeStepTime += (timeStepTime === 1) ? ' minute' : ' minutes';

            duration += (duration === 1) ? ' hour' : ' hours';

            attrs.push({title: 'Start Time: ' + startTime, key: 'Start Time',
                         obj_type: this.get('start_time'), action: 'edit', object: this});

            attrs.push({title: 'Duration: ' + duration, key: 'Duration',
                         obj_type: this.get('obj_type'), action: 'edit', object: this});

            attrs.push({title: 'Time Step: ' + timeStepTime, key: 'Time Step',
                         obj_type: this.get('time_step'), action: 'edit', object: this});

            if (map) {
                attrs.push({title: 'Map:',
                            children: map.toTree(),
                            expanded: true,
                            obj_type: map.get('obj_type'),
                            action: 'new'});
            }

            if (movers) {
                attrs.push({title: 'Movers:',
                            children: movers.toTree(),
                            expanded: true,
                            obj_type: movers.get('obj_type'),
                            action: 'new'});
            }

            if (environment) {
                attrs.push({title: 'Environment:',
                            children: environment.toTree(),
                            expanded: true,
                            obj_type: environment.get('obj_type'),
                            action: 'new'});
            }

            if (weatherers) {
                attrs.push({title: 'Weatherers:',
                            children: weatherers.toTree(),
                            expanded: true,
                            obj_type: weatherers.get('obj_type'),
                            action: 'new'});
            }

            if (spills) {
                attrs.push({title: 'Spills:',
                            children: spills.toTree(),
                            expanded: true,
                            obj_type: spills.get('obj_type'),
                            action: 'new'});
            }

            return attrs;
        },

        isValidAdios: function() {
            return false;
        },

        validWeathering: function() {
            // if (this.get('weathering')){
                // global flag is turned on for the model to be weathering
                // make sure there is at least one weatherer turned on.
                var on_weatherers = this.get('weatherers').filter(function(model){
                    return model.get('on');
                });

                var water = this.get('environment').findWhere({obj_type: 'gnome.environment.water.Water'});
                var element_type = this.getElementType();
                var wind = this.getDefaultWind();

                if (on_weatherers.length > 0 &&
                    element_type && element_type.get('substance') &&
                    water && webgnome.model.get('spills').length > 0 && wind){
                    return true;
                }

            // }

            return false;
        },

        validResponse: function(){
            var skim, burn, disperse;
            if(this.validWeathering()){
                skim = webgnome.model.get('weatherers').findWhere({'obj_type': 'gnome.weatherers.roc.Skim'});
                burn = webgnome.model.get('weatherers').findWhere({'obj_type': 'gnome.weatherers.roc.Burn'});
                disperse = webgnome.model.get('weatherers').findWhere({'obj_type': 'gnome.weatherers.roc.Disperse'});
                if(_.isUndefined(skim) && _.isUndefined(burn) && _.isUndefined(disperse)){
                    return false;
                } else {
                    return true;
                }
            }
            return false;
        },

        resetLocation: function(cb){
            // clear any location relevant objects from the model.

            // reset movers only preserving the wind at the moment.
            var movers = this.get('movers');
            var windMovers = movers.where({obj_type: 'gnome.movers.wind_movers.WindMover'});
            movers.reset(windMovers);

            // remove any environment other than wind and water
            var environment = this.get('environment');
            var winds = environment.where({obj_type: 'gnome.environment.wind.Wind'});
            var water = environment.where({obj_type: 'gnome.environment.water.Water'});
            var waves = environment.where({obj_type: 'gnome.environment.waves.Waves'});
            environment.reset(winds);
            environment.add(water);
            environment.add(waves);

            // drop all of the currents from current outputter
            this.get('outputters').findWhere({obj_type: 'gnome.outputters.json.CurrentJsonOutput'}).get('current_movers').reset();

            // drop all of the ice movers from the ice mover outputter
            this.get('outputters').findWhere({obj_type: 'gnome.outputters.json.IceJsonOutput'}).get('ice_movers').reset();

            // remove the map
            var map = new MapModel({obj_type: 'gnome.map.GnomeMap'});
            this.set('map', map);
            this.save(null, {validate: false, success: cb});
        },

        getDefaultWind: function() {
            // Returns the first object in the environments collection that has 'wind' in it's object type
            // or null if there is nothing that matches
            var env_objs = this.get('environment');
            if (env_objs) {
                return env_objs.find(function(mod){return mod.get('obj_type').toLowerCase().includes('wind');});
            }
            return null;
        },

        getDefaultWater: function() {
            var env_objs = this.get('environment');
            if (env_objs) {
                return env_objs.find(function(mod){return mod.get('obj_type').toLowerCase().includes('water');});
            }
        },

        updateWaves: function(cb){
            var environment = this.get('environment');
            var wind = this.default_env_refs.wind;
            var water = this.default_env_refs.water;

            if(wind && water){

                var waves = environment.findWhere({obj_type: 'gnome.environment.waves.Waves'});
                if(_.isUndefined(waves)){
                    waves = new WavesModel();
                }

                waves.set('wind', wind);
                waves.set('water', water);
                waves.save(null, {
                    validate: false,
                    success: _.bind(function(){
                        environment.add(waves);
                    }, this)
                });
            } else {
                cb();
            }
        },

        populateDefaultEnvRefs: function() {
            if (!this.default_env_refs.windSpecified) {
                this.default_env_refs.wind = this.getDefaultWind();
            } else {
                //if specified, need to make sure it still exists
                if (!this.model.get('environment').contains(this.default_env_refs.wind)){
                    this.default_env_refs.wind = this.getDefaultWind();
                }
            }
            if (!this.default_env_refs.waterSpecified) {
                this.default_env_refs.water = this.getDefaultWater();
            }
        },

        updateOutputters: function(cb){
            // temp add first cats current to the current outputter
            var currents = this.get('movers').where({
                obj_type: 'gnome.movers.current_movers.CatsMover'
            });

            if(currents.length > 0){
                var outputter = this.get('outputters').findWhere({
                    obj_type: 'gnome.outputters.json.CurrentJsonOutput'
                });
                if(outputter){
                    outputter.get('current_movers').add(currents, {merge: true});
                } else {
                    outputter = new CurrentOutputter({current_movers: currents});
                    this.get('outputters').add(outputter);
                }

                this.save(null, {validate: false}).always(cb);
            }
        },

        getCleanup: function() {
            var payload = {
                'Skimmer': [],
                'Burn': [],
                'ChemicalDispersion': []
            };
            var weatherers = this.get('weatherers');
            for (var i = 0; i < weatherers.length; i++) {
                var obj_type = weatherers.at(i).parseObjType();
                if (_.has(payload, obj_type)) {
                    payload[obj_type].push({id: weatherers.at(i).get('id')});
                }
            }

            return payload;
        },

        getElementType: function(){
            if(this.get('spills').length > 0){
                return this.get('spills').at(0).get('element_type');
            } else {
                for(var i in webgnome.obj_ref){
                    if(webgnome.obj_ref[i].get('obj_type') === 'gnome.spill.elements.element_type.ElementType'){
                        return webgnome.obj_ref[i];
                    }
                }
            }
            return false;
        },

        getWinds: function(){
            var env = this.get('environment');
            return _.flatten(
                env.where({'obj_type': 'gnome.environment.wind.Wind'}),
                env.where({'obj_type': 'gnome.environment.environment_objects.GridWind'})
            );
        },

        getTides: function(){
            var environment = this.get('environment');
            return environment.where({'obj_type': 'gnome.environment.tide.Tide'});
        }
    });

    return gnomeModel;
});
