define(['backbone', 'models/TrailModel'],
		function(Backbone, Trail){
	
	var TrailsCollection = Backbone.Collection.extend({
		model: Trail,
		url : "/api/v1/trails/?format=json",
	
		parse: function(response) {
			this.recent_meta = response.meta || {};
			return response.objects || response;
		}
	});
	
	return TrailsCollection;
	
});




