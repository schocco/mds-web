define(['backbone',
        'views/TrailListView',
        'views/TrailDetailView',
        'views/_TrailRatingView',
        'views/TrailUploadView',
        'views/util/MessageMixin',
        'views/auth/AuthView',
        'models/auth/UserModel',
        'views/HomeView',
        'jquery',
        'jquery_cookie',
        'backbone_routefilter'
        ], function(Backbone, TrailListView, TrailDetailView, 
        		TrailRatingView, TrailUploadView, MessageMixin, AuthView, UserModel, HomeView, $){
			// Navigation via router events
			var WorkspaceRouter = Backbone.Router.extend({
				routes: {
					"home":            	"home",
					"udh-scale":        "udh",  
					"uxc-scale": 		"uxc", 
					"mts": 				"mts",
					"trails": 			"trails",
					"trails/upload":	"trail_upload",
					"trails/create":	"trail_create",
					"trails/:id/":		"trail_detail",
					"contact": 			"contact,"
				},

						
				before : function(route, params) {
					console.log("before " + route);
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
				var appRouter = new WorkspaceRouter;
				Backbone.history.start();
				
				
				// add navigate method to views for easy access
				Backbone.View.prototype.goTo = function (loc) {
					appRouter.navigate(loc, true);
				};
				
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

			};
			
			return {
				initialize: initialize
			};
});