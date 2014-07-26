require.config({
	baseUrl: "static/js/app",
	paths: {
		chart: '../chart/Chart.min',
		text: '../require/require.text',
		jquery: '../jquery/jquery-1.10.2.min', 
		underscore: '../underscore/underscore-min', 
		backbone: '../backbone-min.1.0',
		jquery_easing: '../jquery/jquery.easing.1.3',
		jquery_tipsy: '../jquery/jquery.tipsy',
		jquery_form: '../jquery/jquery.form.min',
		jquery_uniform: '../jquery/jquery.uniform',
		jquery_localscroll: '../jquery/jquery.localscroll-1.2.7-min',
		jquery_scrollto: '../jquery/jquery.scrollTo-1.4.3.1-min',
		jquery_modal: '../jquery/jquery.modal.min',
		prettify: '../prettify',
		openlayers: '../openlayers/OpenLayers'
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
