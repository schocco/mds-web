define(['backbone', 'models/trails'],
		function(Backbone, Trail){
	
	var TrailsCollection = Backbone.Collection.extend({
		model: Trail,
		url : "/api/v1/trails/?format=json",
	
		parse: function(response) {
			return response.objects;
		}
	});
	
	return TrailsCollection;
	
});




