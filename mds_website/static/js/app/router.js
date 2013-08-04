define(['backbone',
        'views/trails',
        ], function(Backbone, TrailsView){
			// Navigation via router events
			var WorkspaceRouter = Backbone.Router.extend({
				routes: {
					"/":             	"home",   
					"udh-scale":        "udh",  
					"uxc-scale": 		"uxc", 
					"mts": 				"mts",
					"trails": 			"trails",
					"contact": 			"contact,"
				},
				
				home: function() {
				  console.log("welcome home.");
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
					var trailView = new TrailsView;
					trailView.render();
				},
				
				contact: function() {
					console.log("contact");
				}
			});//end router
			
			var initialize = function(){
				var app_router = new WorkspaceRouter;
				Backbone.history.start();
			};
			
			return {
				initialize: initialize
			};
});