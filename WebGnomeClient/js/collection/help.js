define([
    'underscore',
    'backbone',
    'model/help/help',
    'fuse'
], function(_, Backbone, HelpModel, Fuse){
    'use strict';
    var gnomeHelpCollection = Backbone.Collection.extend({
        model: HelpModel,
        url: '/help',

        search: function(term){
            var options = {keys: ['attributes.keywords'], threshold: 0.65};
            var f = new Fuse(this.models, options);
            var result = f.search(term);
            return result;
        }
    });

    return gnomeHelpCollection;
});