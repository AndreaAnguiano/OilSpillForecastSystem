define([
    'jquery',
    'underscore',
    'backbone',
    'module',
    'views/modal/form',
], function($, _, Backbone, module, FormModal){
    'use strict';
    var customForm = FormModal.extend({

        events: function(){
            return _.defaults({
                'click .option': 'save'
            }, FormModal.prototype.events);
        },

        initialize: function(options){
            if (!_.isUndefined(options.moduleId)) {
                this.module = module;
                this.module.id = options.moduleId;
            }
            FormModal.prototype.initialize.call(this, options);
            var modal = this.el;
            var modaljq = this.$el;

            this.on('ready', function(){
                eval(options.functions.setup); // jshint ignore:line
            }, this);

            this.savefunc = options.functions.save;

        },

        save: function(options) {
            var form = this.$('form');
            var save = eval(this.savefunc); // jshint ignore:line

            if (save) {
                this.error(save);
            } else {
                this.clearError();
                FormModal.prototype.save.call(this, options);
            }
        }
    });

    return customForm;
});