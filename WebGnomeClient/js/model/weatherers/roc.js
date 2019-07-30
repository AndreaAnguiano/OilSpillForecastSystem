define([
    'underscore',
    'backbone',
    'moment',
    'model/weatherers/base'
], function(_, Backbone, moment, BaseWeatherer){
    var ROCWeatherer = BaseWeatherer.extend({

        calculateOperatingPeriods: function(){
            if(webgnome.model){
                var start = moment(webgnome.model.get('start_time'));
                var end = moment(webgnome.model.get('start_time')).add(webgnome.model.get('duration'), 's');
                var days = moment.duration(end.unix() - start.unix(), 'seconds').days();

                var periods = [];
                for(var d = 0; d < days; d++){
                    periods.push([
                        moment(start.format('YYYY-MM-DD') + 'T07:00:00').add(d, 'days').format('YYYY-MM-DDTHH:mm:ss'),
                        moment(start.format('YYYY-MM-DD') + 'T19:00:00').add(d, 'days').format('YYYY-MM-DDTHH:mm:ss')
                    ]);
                }
                return periods;
            }
        },

        isActive: function(datetime){
            var dt_u = moment(datetime).format('X');
            for(var e = 0; e < this.get('timeseries').length; e++){
                var start_ts = moment(this.get('timeseries')[e][0]);
                var end_ts = moment(this.get('timeseries')[e][1]);
                if(start_ts.format('X') <= dt_u && end_ts.format('X') > dt_u){
                    return true;
                }
            }
            return false;
        },

        /**
         * check whether or not the weatherer applies to a given day
         * @param  {String} date YYYY-MM-DD string representation of a day
         * @return {Integer} -1 for false, any other number for index at which to find relevant times
         */
        applies: function(date){
            for(var e = 0; e < this.get('timeseries').length; e++){
                var entry_date = moment(this.get('timeseries')[e][0]);
                if(entry_date.format('Y-M-D') === date){
                    return e;
                }
            }
            return -1;
        },

        /**
         * find the index where a date should be inserted in the timeseries 
         * currently only supports day granularity
         * assumes the timeseries is sorted oldest date to youngest date
         * @param  {String} date YYYY-MM-DD formated string representing the date you wish to insert
         * @return {Integer} 0 to timeseries.length for the index position to insert at
         */
        chronoIndex: function(date){
            var target_date = moment(date);
            for(var e = 0; e < this.get('timeseries').length; e++){
                var entry_date = moment(this.get('timeseries')[e][0]);
                if(target_date.isBefore(entry_date)){
                    return e;
                }
            }

            return this.get('timeseries').length;
        },

        percentToDecimal: function(attr_name){
            return function(model){
                var attr_val = model.get('_' + attr_name);
                if(model.has('_' + attr_name)){
                    model.set(attr_name, model.get('_' + attr_name) / 100, {silent: true});
                }
            };
        },

        decimalToPercent: function(val){
            var per = val * 100;
            return per;
        }
    });

    return ROCWeatherer;
});
