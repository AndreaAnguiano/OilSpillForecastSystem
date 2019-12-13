define([
    'jquery',
    'underscore',
    'backbone',
    'views/modal/base',
    'fancytree'
], function($, _, Backbone, ModalView){
    'use strict';
    var gnomeTreeView = Backbone.View.extend({
        className: 'tree closed',
        open: false,
        debugOn: false,

        events: {
            'click .toggle': 'toggle'
        },

        initialize: function(){
            webgnome.router.views[0].on('debugTreeToggle', _.bind(function(){this.renderModel({attrs: true});}, this), this);
            this.render();

            if (localStorage.getItem('advanced') === 'true'){
                this.toggle();
            }
        },

        render: function(){
            this.$el.html('<div class="toggle">Show Advanced</div><div class="model-tree"><div class="resize"></div></div>');
            this.renderModel();
            webgnome.model.on('sync', this.renderModel, this);
        },

        toggle: function(){
            if(this.open){
                this.open = false;
                this.$el.removeClass('opened').addClass('closed');
                this.$('.toggle').text('Show Advanced');
            } else {
                this.open = true;
                this.$el.addClass('opened').removeClass('closed');
                this.$('.toggle').text('Hide Advanced');
            }

            localStorage.setItem('advanced', this.open);
            this.trigger('toggle');
        },

        renderModel: function(opts){
            if(webgnome.hasModel()){
                if (!_.isUndefined(opts) && _.has(opts, 'attrs')){
                    this.debugOn = !this.debugOn;
                }
                var model_tree;
                if (this.debugOn){
                    model_tree = webgnome.model.toDebugTree();
                } else {
                    model_tree = webgnome.model.toTree();
                }
                if(this.$('.model-tree .ui-fancytree').length === 0){
                    this.$('.model-tree').fancytree({
                        source: model_tree,
                        dblclick: _.bind(function(event, data){
                            var action = data.node.data.action;
                            var form = webgnome.getForm(data.node.data.object.get('obj_type'));
                            var object = data.node.data.object;

                            if(form){
                                if(action === 'edit'){
                                    require([form], _.bind(function(Form){
                                        var view = new Form(null, object);
                                        view.on('hidden', view.close);
                                        view.once('hidden', function(){
                                            webgnome.model.trigger('sync');
                                        });
                                        view.render();
                                    }, this));
                                    
                                } else {
                                    // how am I going to create an object/know what object needs to be created
                                }
                            } else {
                                this.modal = new ModalView({
                                    title: 'No Form Found',
                                    body: 'No form was found to edit or create the object you selected',
                                    buttons: '<a href="" data-dismiss="modal" class="btn btn-primary">Ok</a>'
                                });
                                this.modal.render();
                                console.log('did not find form for ' + object.get('obj_type'));
                            }
                            return false;
                        }, this)
                    });
                } else {
                    this.tree = this.$('div:ui-fancytree').data('uiFancytree').getTree();
                    this.tree.reload(model_tree);
                }
            }
        },

        close: function(){
            if(webgnome.model){
                webgnome.model.off('sync', this.renderModel, this);
            }
            Backbone.View.prototype.close.call(this);
        }
    });

    return gnomeTreeView;
});