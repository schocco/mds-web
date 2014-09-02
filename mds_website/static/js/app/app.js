define(['backbone',
        'router', 
        'collections/MscaleCollection',
        'collections/TrailCollection',
        'views/auth/AuthView',
        'jquery_tipsy', 
        'jquery_localscroll', 
        'jquery_uniform',
        'jquery_pageslide',
        'scrollreveal'
], function(Backbone, Router, MscaleCollection, TrailCollection, AuthView) {
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
		
		
		
//		// Select nav for smaller resolutions
//		// Select menu for smaller screens
//		$("<select />").appendTo("nav#primary");
//
//		// Create default option "Menu"
//		$("<option />", {
//		   "selected": "selected",
//		   "value"   : "",
//		   "text"    : "Menu"
//		}).appendTo("nav#primary select");
//
//		// Populate dropdown with menu items
//		$("nav#primary a").each(function() {
//		 var el = $(this);
//		 $("<option />", {
//		     "value"   : el.attr("href"),
//		     "text"    : el.text()
//		 }).appendTo("nav select");
//		});
//
//		$("nav#primary select").change(function() {
//		  window.location = $(this).find("option:selected").val();
//		});

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
		
		// render authView
		new AuthView();
		
		// init router
		Router.initialize();
	}
	
	return {
		initialize : initialize
	};
});