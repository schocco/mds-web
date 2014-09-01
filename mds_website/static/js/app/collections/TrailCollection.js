define(['backbone', 'models/TrailModel', 'collections/BaseCollection'],
		function(Backbone, Trail, BaseCollection){
	
	var TrailsCollection = BaseCollection.extend({
		model: Trail,
		url : "/api/v1/trails/?format=json"
	});
	
	return TrailsCollection;
	
});




