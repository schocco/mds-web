define(['backbone',
        'views/TrailListView',
        'views/TrailDetailView',
        'views/_TrailRatingView',
        'views/TrailUploadView',
        'views/util/MessageMixin',
        'views/auth/AuthView',
        'views/auth/RedirectView',
        'models/auth/UserModel',
        'views/HomeView',
        'views/generic/_FilterView',
        'jquery',
        'jquery_cookie',
        'backbone_routefilter'
        ], function(Backbone, TrailListView, TrailDetailView, 
        		TrailRatingView, TrailUploadView, MessageMixin, AuthView, RedirectView, UserModel, HomeView, FilterView, $){
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
					"test":				"test"
				},
				
				routes: function(){
					// convert routesPlus to expected format so that router.js does not need
					var routes = [];
					_.each(this.routesPlus, function(value, key, list){
						routes[key] = value.func || value;
					}, this);
					return routes;
				},
				
				test: function(){
					console.log("ztesz");
					var options = {
							el: "#content",
							searchFields: [{field: "name"},
							               {field: "length"}
							],
							filters: [{field: "type", choices: [["dh", "downhill"],["uh", "uphill"]], label: "Type"},
							          {field: "owner", choices: ["rocco"], label: "my uploads"}],
							pageSize: 10
					};
					new FilterView(options);
				},
				
				
				/**
				 * Called before the routing takes place.
				 * Performs auth checks using the routesPlus hash.
				 */
				before: function(route, params) {
					var authRequired = this.routesPlus[route].authRequired
					if(authRequired && !UserModel.currentUser.isAuthenticated()){
						new RedirectView();
						return false;
					}
				},
				
				home: function() {
				    var homeView = new HomeView();
				},
				
				udh: function() {
				  console.log("udh");
				},
				
				uxc: function() {
					console.log("uxc");
				},
				
				mts: function() {
					console.log("mts");
				},
				
				trails: function() {
					console.log("trails");
					var trailView = new TrailListView;
				},
				
				trail_detail: function(id) {
					var trailView = new TrailDetailView({id: id});
				},
				
				trail_upload: function() {
					console.log("trail upload");
					var trailUpView = new TrailUploadView();
				},
				
				trail_create: function() {
					console.log("trail create");
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