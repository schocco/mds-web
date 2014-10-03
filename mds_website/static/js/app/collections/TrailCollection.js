define(['backbone', 'models/TrailModel', 'collections/BaseCollection', 'models/auth/UserModel'],
		function(Backbone, Trail, BaseCollection, UserModel){
	
	var TrailsCollection = BaseCollection.extend({
		model: Trail,
		baseUrl: "/api/v1/trails/",
		searchFields: [{field: "name"}],
		filters: {"type": {choices: [["downhill","downhill"],["xc","cross country"]], label: "type"},
					},
		sortFields: [["name", "name"], ["length","length"]]
		//url : "/api/v1/trails/"
	});
	
	return TrailsCollection;
	
});




