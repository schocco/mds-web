define(['backbone',
        'router', 
        'collections/TrailCollection',
        'collections/MscaleCollection',
        'views/auth/AuthView',
        'module',
        'cache',
        'jquery_tipsy', 
        'jquery_localscroll', 
        'jquery_uniform',
        'jquery_pageslide',
        'scrollreveal',
], function(Backbone, Router, TrailCollection, MscaleCollection, AuthView, module, cache) {
	var initialize = function() {
		

	    // instantiate scrollreveal
	    var config = {
	        after: '0.02s',
	        enter: 'bottom',
	        move: '50px',
	        over: '0.5s',
	        easing: 'ease-in-out',
	        viewportFactor: 0.40,
	        reset: true,
	        init: true
	    };
	    window.scrollReveal = new scrollReveal( config );

		// Responsive menu
	  	$(".open").pageslide();

		// Prettyprint
		$('pre').addClass('prettyprint');
		
		//this is the module conf!
		console.log("module conf in App");
		console.log(module.config());


		// Tipsy
		$('.tooltip').tipsy({
			gravity: $.fn.tipsy.autoNS,
			fade: true,
			html: true
		});

		$('.tooltip-s').tipsy({
			gravity: 's',
			fade: true,
			html: true
		});

		$('.tooltip-e').tipsy({
			gravity: 'e',
			fade: true,
			html: true
		});

		$('.tooltip-w').tipsy({
			gravity: 'w',
			fade: true,
			html: true
		});

		// Scroll
		//jQuery.localScroll();

		// Uniform
		//$("select, input:checkbox, input:radio, input:file").uniform();

		bootstrapMscales();
		
		// init router
		Router.initialize();
	};
	
	
	/**
	 * Sets the bootstrapped mscale collection in the cache.
	 */
	var bootstrapMscales = function(){
		var mscaleJson = module.config().mscaleCollection
		var mscales = new MscaleCollection;
		mscales.reset(mscaleJson);
		cache.set('MscaleCollection', mscales);
	};
	
	return {
		initialize : initialize
	};
});