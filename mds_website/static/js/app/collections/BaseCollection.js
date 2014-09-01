define(['backbone', 'models/TrailModel'],
		function(Backbone, Trail){
	
	var BaseCollection = Backbone.Collection.extend({
	
		parse: function(response) {
			this.recent_meta = response.meta || {};
			return response.objects || response;
		}
	});
	
	return BaseCollection;
	
});




