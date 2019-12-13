define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/default/notfound.html'
], function($, _, Backbone, NotFoundTemplate){
    'use strict';
    var notFoundView = Backbone.View.extend({
        className: 'page notfound',

        initialize: function() {
            this.render();
        },

        render: function(){
            var compiled = _.template(NotFoundTemplate, {email: 'webgnome.help@noaa.gov'});
            $('body').append(this.$el.html(compiled));
        }
    });
    return notFoundView;
});