define(['backbone', 'models/TrailModel', 'collections/BaseCollection'],
		function(Backbone, Trail, BaseCollection){
	
	var TrailsCollection = BaseCollection.extend({
		model: Trail,
		baseUrl: "/api/v1/trails/",
		searchFields: [{field: "name"}],
		filters: [
		          {field: "type", choices: [["downhill","downhill"],["xc","cross country"]], label: "type"},
		          {field: "owner__username", choices: ["rocco"], label: "uploaded by me"}
		          ],
		sorting: [["name", "name"], ["length","length"]]
		//url : "/api/v1/trails/"
	});
	
	return TrailsCollection;
	
});




