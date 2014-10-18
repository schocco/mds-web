define(['backbone',
        'views/TrailListView',
        'views/TrailDetailView',
        'views/TrailUploadView',
        'views/util/MessageMixin',
        'views/auth/AuthView',
        'views/auth/RedirectView',
        'models/auth/UserModel',
        'views/HomeView',
        'views/UdhView',
        'views/UxcView',
        'views/generic/_FilterView',
        'jquery',
        'jquery_cookie',
        'backbone_routefilter'
        ], function(Backbone, TrailListView, TrailDetailView, 
        		TrailUploadView, MessageMixin, 
        		AuthView, RedirectView, UserModel, HomeView,
				UdhView, UxcView, FilterView, $){
	// Navigation via router events
	var WorkspaceRouter = Backbone.Router.extend({

		/**
		 * Each route can be assigned the function to be called or a hash with
		 * additional information. If a hash is used, then it must have the key 'func'.
		 * If the authRequired key is set to true, then an auth check will be
		 * performed before the routing.
		 */
		routesPlus: {
			"home":            	"home",
			"udh-scale":        "udh",  
			"uxc-scale": 		"uxc", 
			"mts": 				"mts",
			"trails": 			"trails",
			"trails/upload":	{func:"trail_upload", authRequired:true},
			"trails/create":	{func:"trail_create", authRequired:true},
			"trails/:id/":		"trail_detail",
			"contact": 			"contact",
		},

		routes: function(){
			// convert routesPlus to expected format so that router.js does not need
			var routes = [];
			_.each(this.routesPlus, function(value, key, list){
				routes[key] = value.func || value;
			}, this);
			return routes;
		},

		

		/**
		 * Called before the routing takes place.
		 * Performs auth checks using the routesPlus hash.
		 */
		before: function(route, params) {
			var authRequired = this.routesPlus[route].authRequired;
			if(authRequired && !UserModel.currentUser.isAuthenticated()){
				new RedirectView();
				return false;
			}
		},

		home: function() {
			var homeView = new HomeView();
		},

		udh: function() {
			var udhView = new UdhView();
		},

		uxc: function() {
			var uxcView = new UxcView();
		},

		mts: function() {
			console.log("mts");
		},

		trails: function() {
			var trailView = new TrailListView;
		},

		trail_detail: function(id) {
			var trailView = new TrailDetailView({id: id});
		},

		trail_upload: function() {
			var trailUpView = new TrailUploadView();
		},

		trail_create: function() {
			//var trailCreateView = new TrailCreateView();
		},

		contact: function() {
			console.log("contact");
		}
	});//end router

	var initialize = function(){
		// add mixin for notifications
		_.extend(Backbone.View.prototype, MessageMixin);	


		// add mixin for notifications
		_.extend(Backbone.View.prototype, MessageMixin);

		//make sure requests have the CSRF token set
		var csrftoken = $.cookie('csrftoken');
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});

		new AuthView;

		//start routing
		var appRouter = new WorkspaceRouter;
		Backbone.history.start();

		// add navigate method to views for easy access
		Backbone.View.prototype.goTo = function (loc) {
			appRouter.navigate(loc, true);
		};


	};

	return {
		initialize: initialize
	};
});