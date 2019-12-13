define([
    'jquery',
    'underscore',
    'backbone',
    'views/wizard/base',
    'views/form/model',
    'views/form/map',
    'views/form/spill',
    'views/form/environment',
    'views/form/random',
    'model/gnome',
    'model/map/map',
    'collection/spills',
], function($, _, Backbone, BaseWizard, ModelForm, MapForm, SpillForm, EnvironmentForm, RandomForm, GnomeModel, GnomeMap, GnomeSpills){
    'use strict';
    var newWizardView = BaseWizard.extend({
        initialize: function(){
            webgnome.model = new GnomeModel();
            webgnome.model.save(null, {
                validate: false,
                error: this.fail,
                success: _.bind(this.setup, this)
            });
        },

        setup: function(){
            this.steps = [
                new ModelForm({
                    name: 'step1',
                    title: 'Model Settings <span class="sub-title">New Model Wizard</span>',
                    buttons: '<button type="button" class="cancel" data-dismiss="modal">Cancel</button><button type="button" class="next">Next</button>',
                }, webgnome.model),
                new MapForm({
                    name: 'step2',
                    title: 'Map <span class="sub-title">New Model Wizard</span>',
                    buttons: '<button type="button" class="cancel" data-dismiss="modal">Cancel</button><button type="button" class="back">Back</button><button type="button" class="next">Next</button>',
                }, webgnome.model.get('map')),
                new SpillForm({
                    name: 'step3',
                    title: 'Spill <span class="sub-title">New Model Wizard</span>',
                    buttons: '<button type="button" class="cancel" data-dismiss="modal">Cancel</button><button type="button" class="back">Back</button><button type="button" class="next">Next</button>',
                }, webgnome.model.get('spills'), webgnome.model.get('map'))
            ];
            this.start();
        },

        fail: function(){
            alert('Unabled to setup a new model on the server!');
            console.log('Unable to setup a new model on the server!');
        }

    });

    return newWizardView;
});