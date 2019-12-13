define([
    'jquery',
    'underscore',
    'backbone',
    'module',
    'moment',
    'cesium',
    'nucos',
    'mousetrap',
    'sweetalert',
    'dropzone',
    'text!templates/default/dropzone.html',
    'text!templates/form/wind.html',
    'text!templates/form/wind/variable-input.html',
    'text!templates/form/wind/variable-static.html',
    'text!templates/form/wind/popover.html',
    'text!templates/uploads/upload.html',
    'text!templates/uploads/upload_activate.html',
    'views/default/cesium',
    'views/modal/form',
    'views/uploads/upload_folder',
    'model/map/graticule',
    'model/movers/wind',
    'model/environment/wind',
    'model/resources/nws_wind_forecast',
    'compassui',
    'jqueryui/widgets/slider',
    'jqueryDatetimepicker'
], function($, _, Backbone, module, moment, Cesium, nucos, Mousetrap, swal,
            Dropzone, DropzoneTemplate, WindFormTemplate,
            VarInputTemplate, VarStaticTemplate, PopoverTemplate,
            UploadTemplate, UploadActivateTemplate,
            CesiumView, FormModal, UploadFolder, Graticule,
            WindMoverModel, WindModel, NwsWind) {
    'use strict';
    var windForm = FormModal.extend({
        title: 'Point Wind',
        className: 'modal form-modal wind-form',
        sliderValue: 0,

        events: function() {
            var formModalHash = FormModal.prototype.events;

            delete formModalHash['change input'];
            delete formModalHash['keyup input'];

            formModalHash['change input:not(tbody input)'] = 'update';
            formModalHash['keyup input:not(tbody input)'] = 'update';

            return _.defaults({
                'shown.bs.tab': 'tabRendered',
                'click .add': 'addTimeseriesEntry',
                'click .edit': 'modifyTimeseriesEntry',
                'click .trash': 'removeTimeseriesEntry',
                'click .ok': 'enterTimeseriesEntry',
                'click .add-row': 'addTimeseriesRow',
                'click .add-another': 'addAnotherEntry',
                'click .undo': 'cancelTimeseriesEntry',
                'click .variable': 'unbindBaseMouseTrap',
                'click .nav-tabs li:not(.variable)': 'rebindBaseMouseTrap',
                'click #extrapolation-allowed': 'setExtrapolation',
                'ready': 'rendered',
                'click .clear-winds': 'clearTimeseries',
                'keyup #nws #lat': 'moveNWSPin',
                'keyup #nws #lon': 'moveNWSPin',
            }, formModalHash);
        },

        initialize: function(options, models) {
            this.module = module;

            FormModal.prototype.initialize.call(this, options);

            if (!_.isUndefined(models)) {
                this.model = models.model;
                this.superModel = models.superModel;
            }
            else {
                this.superModel = new WindMoverModel();
                var windModel = new WindModel();
                this.superModel.set('wind', windModel);
                this.model = this.superModel.get('wind');
            }

            if (!_.isUndefined(this.superModel) &&
                    !this.superModel.get('name')) {
                var count = webgnome.model.get('environment').where({obj_type: this.model.get('obj_type')});
                count = !count ? 1 : count.length + 1;
                this.superModel.set('name', 'Wind #' + count);
                this.model.set('name', 'Wind #' + count);
            }
/*
            this.ol = new OlMapView({
                id: 'wind-form-map',
                zoom: 7,
                center: ol.proj.transform([-137.49, 47.97], 'EPSG:4326', 'EPSG:3857'),
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.TileWMS({
                                url: 'http://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer',
                                params: {'LAYERS': '0', 'TILED': true}
                            })
                    }),
                    new ol.layer.Vector({
                        source: new ol.source.Vector({
                            format: new ol.format.GeoJSON(),
                            url: '/resource/nws_coast.json',
                        }),
                        style: new ol.style.Style({
                            stroke: new ol.style.Stroke({
                                width: 2,
                                color: '#428bca'
                            })
                        })
                    }),
                    this.windLayer,
                    this.spillLayer
                ]
            });
*/
            this.nwsMap = new CesiumView();

            this.$el.on('click', _.bind(function(e) {
                var $clicked = this.$(e.target);

                if (!$clicked.hasClass('add-row') &&
                        $clicked.parents('.popover').length === 0) {
                    this.$('.popover').popover('hide');
                }
            }, this));
            
            this.direction_last_appended = 'down';
            this.heldPin = null;
        },

        render: function(options) {
            var superModelName = 'Not Found';
            if (!_.isUndefined(this.superModel)) {
                superModelName = this.superModel.get('name');
            }

            this.body = _.template(WindFormTemplate, {
                constant_datetime: moment(this.model.get('timeseries')[0][0])
                                   .format(webgnome.config.date_format.moment),
                timeseries: this.model.get('timeseries'),
                unit: this.model.get('units'),
                name: superModelName,
                extrapolation_is_allowed: this.model.get('extrapolation_is_allowed')
            });

            FormModal.prototype.render.call(this, options);

            this.form = {};
            this.form.constant = {};
            this.form.constant.speed = this.$('#constant-speed');
            this.form.constant.direction = this.$('#constant-direction');
            this.form.constant.datetime = this.$('#constant-datetime');
            this.form.variable = {};
            this.form.variable.increment = this.$('#incrementCount');

            this.trigger('show');

            this.$('#constant-datetime').datetimepicker({
                format: webgnome.config.date_format.datetimepicker,
                allowTimes: webgnome.config.date_format.half_hour_times,
                step: webgnome.config.date_format.time_step
            });

            this.$('#datepick').on('click', _.bind(function() {
                this.$('#constant-datetime').datetimepicker('show');
            }, this));

            this.$('select[name="units"]').find('option[value="' + this.model.get('units') + '"]').prop('selected', 'selected');

            setTimeout(_.bind(function() {
                this.$('#constant .slider').slider({
                    min: 0,
                    max: 5,
                    value: 0,
                    create: _.bind(function() {
                        this.$('#constant .ui-slider-handle').html('<div class="tooltip top slider-tip"><div class="tooltip-arrow"></div><div class="tooltip-inner">' + this.model.applySpeedUncertainty(this.model.get('timeseries')[0][1][0]) + '</div></div>');
                    }, this),
                    slide: _.bind(function(e, ui){
                        this.updateConstantSlide(ui);
                    }, this)
                });

                var constantSliderMax = this.$('#constant .slider').slider("option", "max");
                this.$('#constant .slider').slider("option", "value", this.model.get('speed_uncertainty_scale') * (50.0 / 3));
                this.updateTooltipWidth();

            }, this), 1);

            setTimeout(_.bind(function() {
                this.$('#variable .slider').slider({
                    min: 0,
                    max: 5,
                    value: 0,
                    create: _.bind(function() {
                        this.$('#variable .ui-slider-handle').html('<div class="tooltip top slider-tip"><div class="tooltip-arrow"></div><div class="tooltip-inner">+/- ' + this.model.get('speed_uncertainty_scale') * 5.0 + ' %</div></div>');
                    }, this),
                    slide: _.bind(function(e, ui) {
                        this.updateVariableSlide(ui);
                    }, this)
                });

                var variableSliderMax = this.$('#variable .slider').slider("option", "max");

                this.$('#variable .slider').slider("option", "value", this.model.get('speed_uncertainty_scale') * (50.0 / 3));
                this.renderTimeseries();
                this.updateTooltipWidth();                
            }, this), 1);

            //$('.modal').on('scroll', this.variableWindStickyHeader);
            $('.table-wrapper').on('scroll', this.variableWindStickyHeader);

            this.setupUpload();
            this.rendered();
            this.populateDateTime();
        },

        rendered: function() {
            if (this.model.get('timeseries').length <= 1) {
                this.$('.nav-tabs a[href="#constant"]').tab('show');
            }
            else {
                this.unbindBaseMouseTrap();
                this.$('.nav-tabs a[href="#variable"]').tab('show');
            }
        },

        tabRendered: function(e) {
            // preserve the original timeseries if one exists longer than 1 entry
            if (this.model.get('timeseries').length > 1) {
                this.originalTimeseries = this.model.get('timeseries');
            }

            if (_.has(this, 'coords')) {
                delete this.coords;
            }

            if (e.target.hash === '#constant') {
                if (this.$('.constant-compass canvas').length === 0) {
                    this.$('.constant-compass').compassRoseUI({
                        'arrow-direction': 'in',
                        'move': _.bind(this.constantCompassUpdate, this)
                    });

                    this.$('.constant-compass').compassRoseUI('update', {
                        speed: this.form.constant.speed.val(),
                        direction: this.form.constant.direction.val()
                    });
                }
            }
            else if (e.target.hash === '#variable') {
                if (!_.isUndefined(this.originalTimeseries)) {
                    this.model.set('timeseries', this.originalTimeseries);
                }

                this.updateTooltipWidth();
                this.renderTimeseries();
            }
            else if (e.target.hash === '#nws') {
                if (this.$('#wind-form-map canvas').length === 0) {
                    this.$('#wind-form-map').append(this.nwsMap.$el);
                    this.nwsMap.render();

                    //add map polygons
                    var map = webgnome.model.get('map');
                    map.getGeoJSON().then(_.bind(function(data){
                        map.processMap(data, null, this.nwsMap.viewer.scene.primitives);
                    }, this));
                    this.nwsMap.resetCamera(map);

                    //add release pins
                    var spills = webgnome.model.get('spills');
                    for (var s = 0; s < webgnome.model.get('spills').length; s++) {
                        spills.models[s].get('release').generateVis(this.nwsMap.viewer.entities);
                    }

                    this.setupCustomCesiumViewHandlers();
                    //this.renderSpills();

                    this.$('#nws input[name="lat"]').tooltip({
                        trigger: 'focus',
                        html: true,
                        width: 200,
                        placement: 'top',
                        viewport: 'body'
                    });

                    this.$('#nws input[name="lon"]').tooltip({
                        trigger: 'focus',
                        html: true,
                        width: 200,
                        placement: 'top',
                        viewport: 'body'
                    });
                }
            }

            this.update();

            $(window).trigger('resize');

            this.populateDateTime();
        },

        setupCustomCesiumViewHandlers: function() {
            var textPropFuncGen = function(newPin) {
                return new Cesium.CallbackProperty(
                    _.bind(function(){
                        var loc = Cesium.Ellipsoid.WGS84.cartesianToCartographic(this.position._value);
                        var lon, lat;
                        if (this.coordFormat === 'dms') {
                            lon = Graticule.prototype.genDMSLabel('lon', loc.longitude);
                            lat = Graticule.prototype.genDMSLabel('lat', loc.latitude);
                        } else {
                            lon = Graticule.prototype.genDegLabel('lon', loc.longitude);
                            lat = Graticule.prototype.genDegLabel('lat', loc.latitude);
                        }
                        var ttstr = 'Lon: ' + ('\t' + lon) +
                                '\nLat: ' + ('\t' + lat);
                        return ttstr;
                    }, newPin),
                    true
                );
            };
            //add crosshair and forecast pin
            this.nwsCrosshair = this.nwsMap.viewer.entities.add({
                position: Cesium.Cartesian3.fromDegrees(0,0),
                billboard: {
                    image: '/img/crosshair.png',
                    verticalOrigin: Cesium.VerticalOrigin.CENTER,
                    horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
                    width: 30,
                    height: 30,
                },
                show: true,
                coordFormat: 'dms',
                movable: true,
                hoverable: true,
                label : {
                    show : true,
                    showBackground : true,
                    backgroundColor: new Cesium.Color(0.165, 0.165, 0.165, 0.7),
                    font : '14px monospace',
                    horizontalOrigin : Cesium.HorizontalOrigin.LEFT,
                    verticalOrigin : Cesium.VerticalOrigin.TOP,
                    pixelOffset : new Cesium.Cartesian2(2, 0),
                    eyeOffset : new Cesium.Cartesian3(0,0,-5),
                }
            });
            this.nwsCrosshair.label.text = textPropFuncGen(this.nwsCrosshair);
            this.nwsPin = this.nwsMap.viewer.entities.add({
                position: Cesium.Cartesian3.fromDegrees(0,0),
                billboard: {
                    image: '/img/map-pin.png',
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                    horizontalOrigin: Cesium.HorizontalOrigin.CENTER
                },
                show: false,
                coordFormat: 'dms',
                movable: false,
                hoverable: true,
                label : {
                    show : true,
                    showBackground : true,
                    backgroundColor: new Cesium.Color(0.165, 0.165, 0.165, 0.7),
                    font : '14px monospace',
                    horizontalOrigin : Cesium.HorizontalOrigin.LEFT,
                    verticalOrigin : Cesium.VerticalOrigin.TOP,
                    pixelOffset : new Cesium.Cartesian2(2, 0),
                    eyeOffset : new Cesium.Cartesian3(0,0,-5),
                }
            });
            this.nwsPin.label.text = textPropFuncGen(this.nwsPin);

            //alter viewer mouse events to trap the crosshair
            this.nwsMap.pickupEnt(null, this.nwsCrosshair);
            this.nwsMap.mouseHandler.removeInputAction(Cesium.ScreenSpaceEventType.RIGHT_CLICK);
            this.nwsMap.mouseHandler.setInputAction(_.partial(_.bind(this.pickLocation, this.nwsPin), _, this), Cesium.ScreenSpaceEventType.LEFT_CLICK);
        },

        pickLocation: function(movement, view) {
            //this context should always be an entity
            var newPos = view.nwsMap.viewer.scene.camera.pickEllipsoid(movement.position);
            this.position = newPos;
            this.show = true;
            this.label.show = true;
            var coords = Cesium.Ellipsoid.WGS84.cartesianToCartographic(newPos);
            coords = {lon: Cesium.Math.toDegrees(coords.longitude),
                      lat: Cesium.Math.toDegrees(coords.latitude)};
            view.$('#nws #lat').val(coords.lat);
            view.$('#nws #lon').val(coords.lon);
            view.nwsFetch(coords);
            view.trigger('newNWS', this, coords);
            view.nwsMap.viewer.scene.requestRender();
        },

        moveNWSPin: function(e) {
            var coords = [this.$('#nws #lon').val(),this.$('#nws #lat').val()];
            coords = this.coordsParse(_.clone(coords));

            if (_.isNaN(coords[0])) {
                coords[0] = 0;
            }

            if (_.isNaN(coords[1])) {
                coords[1] = 0;
            }
            coords = {lon: coords[0], lat: coords[1]};

            this.nwsPin.position = Cesium.Cartesian3.fromDegrees(coords.lon, coords.lat);
            this.nwsPin.show = true;
            this.nwsMap.viewer.scene.requestRender();
            this.nwsFetch(coords);
        },

        showParsedCoords: function(coords) {
            this.$('.lat-parse').text('(' + coords[1].toFixed(4) + ')');
            this.$('.lon-parse').text('(' + coords[0].toFixed(4) + ')');
        },

        coordsParse: function(coordsArray) {
            for (var i = 0; i < coordsArray.length; i++) {
                if (!_.isUndefined(coordsArray[i]) &&
                        coordsArray[i].trim().indexOf(' ') !== -1) {
                    coordsArray[i] = nucos.sexagesimal2decimal(coordsArray[i]);
                    coordsArray[i] = parseFloat(coordsArray[i]);
                }
                else if (!_.isUndefined(coordsArray[i])) {
                    coordsArray[i] = parseFloat(coordsArray[i]);
                }
            }

            return coordsArray;
        },

        populateDateTime: function() {
            var timeseries = this.model.get('timeseries');
            var starting_time = timeseries[timeseries.length - 1][0];

            this.$('#variable-datetime').val(moment(starting_time).format(webgnome.config.date_format.moment));
        },

        nwsSubmit: function(e) {
            e.preventDefault();
            // var coords = {};
            // coords.lat = parseFloat(this.$('#nws #lat').val());
            // coords.lon = parseFloat(this.$('#nws #lon').val());
            this.updateNWSMap(e);
        },

        nwsFetch: function(coords) {
            this.nws = new NwsWind(coords);
        },

        setupUpload: function(obj_type) {
            this.$('#upload_form').empty();

            if (webgnome.config.can_persist) {
                this.$('#upload_form').append(_.template(UploadActivateTemplate,
                                              {page: false}));
            }
            else {
                this.$('#upload_form').append(_.template(UploadTemplate));
            }

            if (!obj_type) {
                obj_type = WindMoverModel.prototype.defaults.obj_type;
            }

            this.dropzone = new Dropzone('.dropzone', {
                url: webgnome.config.api + '/mover/upload',
                previewTemplate: _.template(DropzoneTemplate)(),
                paramName: 'new_mover',
                maxFiles: 1,
                //acceptedFiles: '.osm, .wnd, .txt, .dat',
                dictDefaultMessage: 'Drop file here to upload (or click to navigate)<br>Supported formats: all' //<code>.wnd</code>, <code>.osm</code>, <code>.txt</code>, <code>.dat</code>'
            });

            this.dropzone.on('sending', _.bind(this.sending,  {obj_type: obj_type}));
            this.dropzone.on('uploadprogress', _.bind(this.progress, this));
            this.dropzone.on('error', _.bind(this.reset, this));
            this.dropzone.on('success', _.bind(this.loaded, this));

            if (webgnome.config.can_persist) {
                this.uploadFolder = new UploadFolder({el: $(".upload-folder")});
                this.uploadFolder.on("activate-file", _.bind(this.activateFile, this));
                this.uploadFolder.render();
            }
        },

        sending: function(e, xhr, formData, obj_type) {
            formData.append('session', localStorage.getItem('session'));
            formData.append('obj_type', this.obj_type);
            formData.append('persist_upload',
                            $('input#persist_upload')[0].checked);
        },

        progress: function(e, percent) {
            if (percent === 100) {
                this.$('.dz-preview').addClass('dz-uploaded');
                this.$('.dz-loading').fadeIn();
            }
        },

        reset: function(file, err) {
            var errObj = JSON.parse(err);
            console.error(errObj);

            this.$('.dz-error-message span')[0].innerHTML = (errObj.exc_type +
                                                             ': ' +
                                                             errObj.message);

            setTimeout(_.bind(function() {
                this.$('.dropzone').removeClass('dz-started');
                this.dropzone.removeFile(file);
            }, this), 3000);
        },

        loaded: function(e, response) {
            var json_response = JSON.parse(response);
            var mover;

            if (json_response && json_response.obj_type) {
                if (json_response.obj_type === WindMoverModel.prototype.defaults.obj_type) {
                    mover = new WindMoverModel(json_response, {parse: true});
                    //this.model = json_response['wind'];
                }
                this.trigger('save', mover);
            }
            else {
                console.error('No response to file upload');
            }

            this.hide();
        },

        activateFile: function(filePath) {
            if (this.$('.popover').length === 0) {
                var thisForm = this;

                $.post('/environment/activate', {'file-name': filePath})
                .done(function(response) {
                    thisForm.loaded(filePath, response);
                });
            }
        },
    
        nwsLoad: function(model) {
            this.model.set('timeseries', model.get('timeseries'));
            this.model.set('units', model.get('units'));

            this.$('.variable a').tab('show');

            this.unbindBaseMouseTrap();

            this.$('.save').removeClass('disabled');

            this.populateDateTime();
            this.save();
        },

        nwsError: function() {
            this.error('Error!', 'No NWS forecast data found');
            this.$('.save').removeClass('disabled');
        },

        update: function(compass) {
            var active = this.$('.nav-tabs.wind .active a').attr('href').replace('#', '');

            if (active === 'constant') {
                var speed = this.form[active].speed.val();
                var direction = this.form[active].direction.val();

                if (direction.match(/[s|S]|[w|W]|[e|E]|[n|N]/) !== null) {
                    direction = this.$('.' + active + '-compass')[0].settings['cardinal-angle'](direction);
                }

                var gnomeStart = webgnome.model.get('start_time');

                if (compass && speed !== '' && direction !== '') {
                    this.$('.' + active + '-compass').compassRoseUI('update', {
                        speed: speed,
                        direction: direction,
                        trigger_move: false
                    });
                }

                // if the constant wind pane is active, a timeseries
                // needs to be generated for the values provided
                var dateObj = moment(this.form.constant.datetime.val(),
                                     webgnome.config.date_format.moment);
                var date = dateObj.format('YYYY-MM-DDTHH:mm:00');

                this.model.set('timeseries', [[date, [speed, direction]]]);
                this.updateConstantSlide();


                this.model.set('units', this.$('#' + active + ' select[name="units"]').val());
                this.model.set('name', this.$('#name').val());
                this.superModel.set('name', this.$('#name').val());
                
                this.$('.additional-wind-compass').remove();
            }

            if (active === 'variable') {
                var currentUnits = this.$('#' + active + ' select[name="units"]').val();

                this.$('#' + active + ' .units').text('(' + currentUnits + ')');
                this.model.set('units', this.$('#' + active + ' select[name="units"]').val());
                this.model.set('name', this.$('#name').val());
                this.superModel.set('name', this.$('#name').val());
            }
        },

        updateVariableSlide: function(ui) {
            var value;

            if (this.$('#variable .ui-slider').length === 0) {return null;}

            if (!_.isUndefined(ui)) {
                value = ui.value;
            }
            else {
                value = !_.isUndefined(this.sliderValue) ? this.sliderValue : this.$('#variable .slider').slider('value');
            }

            this.sliderValue = value;
            var percentRange = this.sliderValue * 3.0;

            this.$('#variable .tooltip-inner').text('+/- ' + percentRange.toFixed(1) + ' %');

            var variableSliderMax = this.$('#variable .slider').slider("option", "max");

            this.model.set('speed_uncertainty_scale', this.sliderValue / (50.0 / 3));

            this.$('#variable .slider').slider('value', this.sliderValue);

            this.renderTimeseries(value);
            this.updateTooltipWidth();
        },

        updateConstantSlide: function(ui) {
            var value;

            if (this.$('#constant .ui-slider').length === 0) {return null;}

            if (!_.isUndefined(ui)) {
                value = ui.value;
            }
            else {
                value = !_.isUndefined(this.sliderValue) ? this.sliderValue : this.$('#constant .slider').slider('value');
            }

            this.sliderValue = value;

            if (this.model.get('timeseries').length > 0) {
                var speed = this.model.get('timeseries')[0][1][0];
                var uncertainty = this.sliderValue / (50.0 / 3);

                if (this.sliderValue === 0) {
                    this.$('#constant .tooltip-inner').text(speed);
                }
                else {
                    var rangeObj = nucos.rayleighDist().rangeFinder(speed, uncertainty);
                    this.$('#constant .tooltip-inner').text(rangeObj.low.toFixed(1) + ' - ' + rangeObj.high.toFixed(1));
                }

                var constantSliderMax = this.$('#constant .slider').slider("option", "max");

                this.model.set('speed_uncertainty_scale', uncertainty);
                this.$('#constant .slider').slider('value', this.sliderValue);

                this.updateTooltipWidth();
            }
        },

        constantCompassUpdate: function(magnitude, direction) {
            this.form.constant.speed.val(parseInt(magnitude, 10));
            this.form.constant.direction.val(parseInt(direction, 10));
            this.update(false);
        },

        variableCompassUpdate: function(magnitude, direction) {
            this.form.variable.speed.val(parseInt(magnitude, 10));
            this.form.variable.direction.val(parseInt(direction, 10));
            this.update(false);
        },

        modifyTimeseriesEntry: function(e, rowIndex) {
            // Create boolean value to confirm that the DOM element clicked
            // was the  edit pencil and not the check in the table row.
            var editClassExists = this.$(e.target).hasClass('edit');

            if ((this.$('.input-speed').length === 0 && editClassExists) ||
                    !_.isUndefined(rowIndex)) {
                var row;
                var index;

                if (editClassExists) {
                    e.preventDefault();
                    row = this.$(e.target).parents('tr')[0];
                    index = this.$(row).data('tsindex');
                }
                else if (!_.isUndefined(rowIndex)) {
                    index = rowIndex >= 0 ? rowIndex : 0;
                    row = this.$('[data-tsindex="' + index + '"]');
                }

                var entry = this.model.get('timeseries')[index];
                var date = moment(entry[0]).format(webgnome.config.date_format.moment);

                var compiled = _.template(VarInputTemplate);
                var template = compiled({
                    'date': date,
                    'speed': entry[1][0],
                    'direction': entry[1][1]
                });

                this.$(row).addClass('edit');
                this.$(row).removeClass('error');
                this.$(row).html(template);
                this.$(row).find('.input-time').datetimepicker({
                    format: webgnome.config.date_format.datetimepicker,
                    allowTimes: webgnome.config.date_format.half_hour_times,
                    step: webgnome.config.date_format.time_step
                });

                this.$('tr .add-row').remove();
                this.$(row).find('.input-speed').focus().val(entry[1][0]);
                this.attachCompass(e, entry, row);
            }
        },

        addRowHelper: function(e, index, newIndex, opts) {
            this.model.addTimeseriesRow(index, newIndex, opts);
            this.renderTimeseries();

            if (index - newIndex >= 0) {
                this.modifyTimeseriesEntry(e, index);
                this.direction_last_appended = 'up';
            }
            else {
                this.modifyTimeseriesEntry(e, newIndex);
                this.direction_last_appended = 'down';
            }
        },

        addTimeseriesRow: function(e) {
            if (this.$('.popover').length === 0) {
                var parentRow = this.$(e.target).parents('tr')[0];
                var index = this.$(parentRow).data('tsindex');

                var compiled = _.template(PopoverTemplate, {
                    tsindex: index
                });

                this.$(e.target).popover({
                    placement: 'left',
                    html: 'true',
                    title: '<span class="text-info"><strong>Add Row</strong></span>',
                    content: compiled,
                    trigger: 'click focus'
                });

                this.$(e.target).popover('show');

                var interval = this.$('#incrementCount').val();

                this.$('.above').on('click', _.bind(function(e) {
                    var newIndex = index - 1;
                    this.addRowHelper(e, index, newIndex, {'interval': interval});
                    this.direction_last_appended = 'up';
                }, this));

                this.$('.below').on('click', _.bind(function(e) {
                    var newIndex = index + 1;
                    this.addRowHelper(e, index, newIndex, {'interval': interval});
                    this.direction_last_appended = 'down';
                }, this));

                this.$('.popover').one('hide.bs.popover', _.bind(function() {
                    this.$('.above').off('click');
                    this.$('.below').off('click');
                }, this));
            }
        },

        clearTimeseries: function(e) {
            e.preventDefault();
            var model_start_time = webgnome.model.get('start_time');

            swal({
                title: 'Are you sure?',
                text: 'This action will delete the all of the wind entries below.',
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: "Yes, delete it.",
                closeOnConfirm: true
            }).then(_.bind(function(isConfirm) {
                if (isConfirm) {
                    this.model.set('timeseries', [[model_start_time, [0, 0]]]);
                    this.originalTimeseries = [[model_start_time, [0, 0]]];
                    this.renderTimeseries();
                }
            }, this));
        },

        attachCompass: function(e, entry, row) {
            this.$el.off('keyup tr input');
            this.entry = entry;

            var top = (this.$('.modal-content').offset().top * -1) + this.$(row).offset().top + this.$(row).outerHeight();
            var right = 26 + "px";

            this.$('.modal-content').append('<div class="additional-wind-compass"></div>');

            this.$('.additional-wind-compass').compassRoseUI({
                    'arrow-direction': 'in',
                    'move': _.bind(this.variableRoseUpdate, this)
                });

            this.$('.additional-wind-compass').css({"position": "absolute",
                                                    "right": right,
                                                    "top": top});
            this.$el.on('keyup tr input', _.bind(this.writeValues, this));

            this.writeValues();
        },

        writeValues: function() {
            var direction = this.$('.input-direction').val();

            if (direction.match(/[s|S]|[w|W]|[e|E]|[n|N]/) !== null) {
                direction = this.$('.additional-wind-compass')[0].settings['cardinal-angle'](direction);
            }

            this.$('.additional-wind-compass').compassRoseUI('update', {
                speed: this.$('.input-speed').val(),
                direction: direction
            });
        },

        variableRoseUpdate: function(magnitude, direction) {
            this.$('.input-speed').val(parseInt(magnitude, 10));
            this.$('.input-direction').val(parseInt(direction, 10));
        },

        enterTimeseriesEntry: function(e) {
            e.preventDefault();
            var row;

            if (e.which === 13) {
                row = this.$('tr.edit')[0];
            }
            else {
                row = this.$(e.target).parents('tr')[0];
            }

            if (!_.isUndefined(row)) {
                var index = $(row).data('tsindex');
                var entry = this.model.get('timeseries')[index];
                var speed = this.$('.input-speed').val();
                var direction = this.$('.input-direction').val();

                var date = moment(this.$('.input-time').val(),
                                  'YYYY/MM/DD HH:mm').format('YYYY-MM-DDTHH:mm:00');

                if (direction.match(/[s|S]|[w|W]|[e|E]|[n|N]/) !== null) {
                    direction = this.$('.additional-wind-compass')[0].settings['cardinal-angle'](direction);
                }

                entry = [date, [speed, direction]];
                var tsCopy = _.clone(this.model.get('timeseries'));

                _.each(tsCopy, _.bind(function(el, i, array) {
                    if (index === i) {
                        array[i] = entry;
                    }
                }, this));

                this.model.set('timeseries', tsCopy);
                this.$('.additional-wind-compass').remove();

                $('.xdsoft_datetimepicker:last').remove();
                $(row).remove();

                this.renderTimeseries();
            }
        },

        addAnotherEntry: function(e) {
            e.preventDefault();
            var row;

            if (e.which === 13) {
                row = this.$('tr.edit')[0];
            }
            else {
                row = this.$(e.target).parents('tr')[0];
            }

            var index;

            if (!_.isUndefined(row)) {
                index = $(row).data('tsindex');

                var entry = this.model.get('timeseries')[index];
                var speed = this.$('.input-speed').val();
                var direction = this.$('.input-direction').val();

                var date = moment(this.$('.input-time').val(),
                                  'YYYY/MM/DD HH:mm').format('YYYY-MM-DDTHH:mm:00');
 
                if (direction.match(/[s|S]|[w|W]|[e|E]|[n|N]/) !== null) {
                    direction = this.$('.additional-wind-compass')[0].settings['cardinal-angle'](direction);
                }

                entry = [date, [speed, direction]];

                var tsCopy = _.clone(this.model.get('timeseries'));
                _.each(tsCopy, _.bind(function(el, i, array) {
                    if (index === i) {
                        array[i] = entry;
                    }
                }, this));

                this.model.set('timeseries', tsCopy);
                this.$('.additional-wind-compass').remove();

                $('.xdsoft_datetimepicker:last').remove();
                //$(row).remove();
                //this.renderTimeseries();
            }

            var parentRow = this.$(e.target).parents('tr')[0];
            index = this.$(parentRow).data('tsindex');

            var interval = this.$('#incrementCount').val();
            var nextIndex = index + 1;

            if (this.direction_last_appended === 'up') {
                nextIndex = index - 1;
            }

            this.addRowHelper(e, index, nextIndex, {'interval': interval});
            
        },

        cancelTimeseriesEntry: function(e) {
            e.preventDefault();
            var row = this.$(e.target).parents('tr')[0];
            var index = $(row).data('tsindex');
            var entry = this.model.get('timeseries')[index];

            this.renderTimeseries();

            this.$('.additional-wind-compass').compassRoseUI('update', {
                speed: entry[1][0],
                direction: entry[1][1]
            });

            this.$(row).removeClass('edit');
            this.$('.additional-wind-compass').remove();

            $('.xdsoft_datetimepicker:last').remove();
        },

        removeTimeseriesEntry: function(e) {
            if (this.$('.input-speed').length === 0) {
                e.preventDefault();
                e.stopPropagation();
                var model_start_time = webgnome.model.get('start_time');
                var index = $(e.target.parentElement.parentElement).data('tsindex');
                this.model.get('timeseries').splice(index, 1);
                this.model.trigger('change', this.model);
                if(this.model.get('timeseries').length === 0){
                    this.model.set('timeseries', [[model_start_time, [0, 0]]]);
                }
                this.renderTimeseries();
            }
        },

        renderTimeseries: function(uncertainty) {
            if (this.$('#variable .ui-slider').length === 0) {return null;}

            if (!_.isUndefined(uncertainty)) {
                uncertainty = uncertainty / (50.0 / 3);
            }

            if (_.isUndefined(uncertainty)) {
                uncertainty = this.$('#variable .slider').slider('value') / (50.0 / 3);
            }

            var html = '';

            _.each(this.model.get('timeseries'), function(el, index) {
                var velocity = el[1][0];
                var direction = el[1][1];

                if (uncertainty > 0) {
                    var rangeObj = nucos.rayleighDist().rangeFinder(velocity, uncertainty);
                    var low = rangeObj.low.toFixed(1);
                    var high = rangeObj.high.toFixed(1);

                    if (low < 0) {
                        low = 0;
                    }

                    velocity = low + ' - ' + high;
                }

                var date = moment(el[0]).format(webgnome.config.date_format.moment);

                var compiled = _.template(VarStaticTemplate, {
                    tsindex: index,
                    date: date,
                    speed: velocity,
                    direction: direction
                });

                html = html + compiled;
            });

            this.$('table:first tbody').html(html);

            var invalidEntries = this.model.validateTimeSeries();

            _.each(invalidEntries, _.bind(function(el, index) {
                this.$('[data-tsindex="' + el + '"]').addClass('error');
            }, this));
        },

        unbindBaseMouseTrap: function() {
            Mousetrap.unbind('enter');
            Mousetrap.bind('enter', _.bind(this.enterTimeseriesEntry, this));
        },

        rebindBaseMouseTrap: function() {
            Mousetrap.unbind('enter');
            Mousetrap.bind('enter', _.bind(this.submitByEnter, this));
        },

        variableWindStickyHeader: function(e) {
            if ($('.wind-form #variable table:visible').length > 0) {
                var top = $('.table-wrapper').scrollTop();

                if (top > 0 && $('.wind-form .sticky').length === 0) {
                    // add a sticky header to the table.
                    $('<div class="sticky"><table class="table table-condensed">' + $('.wind-form #variable table:last').html() + '</table></div>').appendTo('.wind-form #variable .table-wrapper');
                }
                else if (top === 0 && $('.wind-form #variable .sticky').length > 0) {
                    // remove the sticky header from the table.
                    $('.wind-form #variable .sticky').remove();
                }
                else {
                    $('.wind-form #variable .sticky').css('top', top + 'px');
                }
            }
        },

        setExtrapolation: function(e) {
            var selected = $(e.target).is(':checked');
            this.model.set('extrapolation_is_allowed', selected);
        },

        save: function() {
            if (_.isUndefined(this.nws) || this.nws.fetched) {
                //this.update();

                FormModal.prototype.save.call(this);
            }
            else {
                this.$('.save').addClass('disabled');

                this.nws.fetch({
                    success: _.bind(this.nwsLoad, this),
                    error: _.bind(this.nwsError, this)
                });

                this.nws.fetched = true;
            }
        },

        back: function() {
            $('.xdsoft_datetimepicker:last').remove();

            FormModal.prototype.back.call(this);
        },

        close: function() {
            $('.xdsoft_datetimepicker:last').remove();
            $('.xdsoft_datetimepicker:last').remove();
            $('.modal').off('scroll', this.variableWindStickyHeader);
            
            if (this.nws) {
                this.nws.cancel();
            }

            if (this.dropzone) {
                this.dropzone.disable();
            }
            
            $('input.dz-hidden-input').remove();

            FormModal.prototype.close.call(this);
        },
    });

    return windForm;
});
