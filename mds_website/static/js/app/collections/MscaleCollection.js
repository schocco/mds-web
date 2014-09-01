define(['backbone', 'models/MscaleModel', 'collections/BaseCollection'],
		function(Backbone, Mscale, BaseCollection){
	
	var MscaleCollection = BaseCollection.extend({
		model: Mscale,
		url : "/api/v1/mscales/?format=json"
	});
	
	return MscaleCollection;
	
});




