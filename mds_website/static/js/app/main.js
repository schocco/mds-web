require.config({
	baseUrl: "static/js/app",
	paths: {
		chart: '../chart/Chart.min',
		text: '../require/require.text',
		jquery: '../jquery/jquery-1.10.2.min', 
		underscore: '../underscore/underscore-min', 
		backbone: '../backbone-min.1.0',
		backbone_routefilter: '../backbone.routefilter-0.2.1.min',
		jquery_easing: '../jquery/jquery.easing.1.3',
		jquery_tipsy: '../jquery/jquery.tipsy',
		jquery_form: '../jquery/jquery.form.min',
		jquery_uniform: '../jquery/jquery.uniform',
		jquery_localscroll: '../jquery/jquery.localscroll-1.3.5-min',
		jquery_scrollto: '../jquery/jquery.scrollTo-1.4.13-min',
		jquery_pageslide: '../jquery/jquery.pageslide.min',
		jquery_modal: '../jquery/jquery.modal.min',
		jquery_cookie: '../jquery/jquery.cookie.1.4.1',
		prettify: '../prettify',
		openlayers: '../openlayers/OpenLayers',
		scrollreveal: '../scrollreveal/scrollReveal'
	},
	    shim: {
	    	'chart': {
	    		exports: 'chart'
	    	},
	        'backbone': {
	            deps: ['underscore', 'jquery'],
	            //Once loaded, use the global 'Backbone' as the
	            //module value.
	            exports: 'Backbone'
	        },
	        'underscore': {
	            exports: '_'
	        },
	        'openlayers': {
	        	exports: 'OpenLayers'
	        },
	        'jquery': {
	        	exports: '$'
	        },
	        'jquery_easing': ['jquery'],
	        'jquery_pageslide': ['jquery'],
	        'jquery_tipsy':  ['jquery'],
	        'jquery_uniform': ['jquery'],
	        'jquery_form': ['jquery'],
	        'jquery_localscroll': ['jquery'],
	        'jquery_scrollto': ['jquery'],
	        'jquery_modal': ['jquery']
	    }
});

require([
	'app',
    ], function(App){
		App.initialize();
	}
);
