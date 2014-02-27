define(['backbone',
        'views/TrailListView',
        'views/TrailDetailView',
        'views/_TrailRatingView',
        'views/TrailUploadView',
        ], function(Backbone, TrailListView, TrailDetailView, TrailRatingView, TrailUploadView){
			// Navigation via router events
			var WorkspaceRouter = Backbone.Router.extend({
				routes: {
					"home":            	"home",   
					"udh-scale":        "udh",  
					"uxc-scale": 		"uxc", 
					"mts": 				"mts",
					"trails": 			"trails",
					"trails/upload":	"trail_upload",
					"trails/:id/rate":	"trail_rate",
					"trails/:id":		"trail_detail",
					"contact": 			"contact,"
				},
				
				home: function() {
				  console.log("welcome home.");
				  //var homeView = new HomeView();
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
				
				trail_rate: function(id) {
					console.log("rate trail with id" + id);
					var trailView = new TrailRatingView({id: id});
				},
				
				trail_detail: function(id) {
					console.log("trail_detail for id " + id);
					var trailView = new TrailDetailView({id: id});
				},
				
				trail_upload: function() {
					console.log("trail upload");
					var trailUpView = new TrailUploadView();
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


			};
			
			return {
				initialize: initialize
			};
});