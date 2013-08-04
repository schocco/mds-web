define(['backbone', 'collections/trails'],
		function(Backbone, TrailsCollection){
	
	var TrailsView = Backbone.View.extend({
		el: '.one_full',
		initialize: function () {
			// isLoading is a useful flag to make sure we don't send off more than 
			// one request at a time 
			console.log("init trailsview");
			this.trailsCollection = new TrailsCollection();
		},
		render: function(){
			console.log("render trails view");
			this.loadTrails();
		},
		loadTrails: function(){
			var that = this;
			this.trailsCollection.fetch({
				success: function (trails) {
					$(that.el).append("trails");
					that.isLoading = false;
				}
			});
		}
			
	});
	
	return TrailsView;
	
});


