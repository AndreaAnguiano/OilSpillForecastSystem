define([
    'underscore',
    'jquery',
    'backbone'
], function(_, $, Backbone) {
    'use strict';
    var nwsWind = Backbone.Model.extend({
        fetching: false,
        fetched: false,

        initialize: function(options) {
            Backbone.Model.prototype.initialize.call(this, options);
            this.on('sync error', this.resetFetch, this);
        },

        url: function() {
            return webgnome.config.goods_api + '/winds/NWS_point/point_forecast?format=JSON';
        },

        validate: function(attrs, options) {
            if (_.isUndefined(attrs.lat) || _.isUndefined(attrs.lon)) {
                return 'Latitude and Longitude are both required.';
            }
        },

        fetch: function(options) {
            if (this.isValid()) {
                if (_.isUndefined(options)) {
                    options = {};
                }

                if (!_.has(options, 'data')) {
                    options.data = {
                        'latitude': this.get('lat'),
                        'longitude': this.get('lon')
                    };
                }
                else {
                    options.data.latitude = this.get('lat');
                    options.data.longitude = this.get('lon');
                }

                this.fetching = true;
                this.request = Backbone.Model.prototype.fetch.call(this, options);
            }
        },

        cancel: function() {
            if (this.fetching && this.request) {
                this.request.abort();
                this.resetFetch();
            }
        },

        resetFetch: function() {
            this.fetching = false;
        }
    });

    return nwsWind;
});
