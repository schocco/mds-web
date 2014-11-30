define(['backbone',
        'router', 
        'collections/TrailCollection',
        'collections/MscaleCollection',
        'models/auth/UserModel',
        'models/auth/UserSessionMonitor',
        'module',
        'cache',
        'jquery-tipsy', 
        'sidr',
        'scrollReveal',
        'jquery-touchswipe'
], function(Backbone, Router, TrailCollection, MscaleCollection, UserModel,UserSessionMonitor, module, cache) {
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
        $("#mobile-nav-open").sidr({
            source : "#menu-source",
            displace : false
        });
        $(window).swipe({
            fallbackToMouseEvents : false,
            //Generic swipe handler for all directions
            swipeLeft : function(event, direction, distance, duration, fingerCount) {
                $.sidr("close");
            },
            swipeRight : function(event, direction, distance, duration, fingerCount) {
                $.sidr("open");
            },
        }); 



		// Prettyprint
		$('pre').addClass('prettyprint');
		
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

		bootstrapMscales();
		setCurrentUser();
		
		// init router
		Router.initialize();
	};
	
	
	/**
	 * Sets the bootstrapped mscale collection in the cache.
	 */
	var bootstrapMscales = function(){
		var mscaleJson = module.config().mscaleCollection;
		var mscales = new MscaleCollection;
		mscales.reset(JSON.parse(mscaleJson));
		console.log(mscales);
		cache.set('MscaleCollection', mscales);
	};
	
	/**
	 * Reads the bootstrapped user object and sets it as static field
	 * on the UserModel class.
	 * 
	 * Listens for logout event to reset the user when a logout occurs.
	 * Listens for login events to set the user when a login occurs.
	 */
	var setCurrentUser = function(){
		var userJson = module.config().current_user;
	    var user = new UserModel(JSON.parse(userJson));
		
		UserModel.currentUser = user;
		//start monitoring the user session
		UserSessionMonitor.start();
		console.log("set user. ");
	};
	
	return {
		initialize : initialize
	};
});