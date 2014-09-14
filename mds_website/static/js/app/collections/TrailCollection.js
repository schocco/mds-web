define(['backbone', 'models/TrailModel', 'collections/BaseCollection'],
		function(Backbone, Trail, BaseCollection){
	
	var TrailsCollection = BaseCollection.extend({
		model: Trail,
		baseUrl: "/api/v1/trails/"
		//url : "/api/v1/trails/"
	});
	
	return TrailsCollection;
	
});




