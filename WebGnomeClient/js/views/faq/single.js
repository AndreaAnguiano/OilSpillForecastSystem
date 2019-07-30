define([
    'jquery',
    'underscore',
    'backbone',
    'chosen',
    'views/default/help',
    'text!templates/faq/specific.html',
    'model/help/help'
], function($, _, Backbone, chosen, HelpView, SpecificTemplate, HelpModel){
    'use strict';
	var singleFAQView = HelpView.extend({
		className: 'helpcontent',
		id: 'support',

		events: function(){
			return _.defaults({}, HelpView.prototype.events);
		},

		initialize: function(options){
			this.topic = options.topic;
			this.help = new HelpModel({id: this.topic.path});
			this.render();
		},

		render: function(){
			var data = this.topic;
			$('#support').html('');
			var compiled = _.template(SpecificTemplate, {title: data.title, content: data.content, keywords: data.keywords });
			$('#support').append(this.$el.html(compiled));
		}
	});
	return singleFAQView;
});