odoo.define('train.Activity', function(require) {
    'use strict';
    
    require('web.dom_ready');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var WebClient = require('web.WebClient');

   console.log("HELLO : train.js file loaded");

    var MyWidget = Widget.extend({
        init: function(parent, value){
            this._super(parent);
            this.count = value;
            //debugger;
            console.log("Widget MyWidget started with value "+this.count);
        },
        start : function(){
            console.log("Inside MyWidget start()");
            //alert("Inside MyWidget");
        },
        onClick : function(){
            this.count++;
            console.log("Button clicked "+this.count+" times! ");
            this.$('.val').text(this.count);
        },
        template: 'testsss',
        events : {
            'click button' : 'onClick',
        },
    });
       
    var temp = new MyWidget(this, 5);
    temp.appendTo($('body'));

});