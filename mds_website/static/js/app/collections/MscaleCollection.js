define(['backbone', 'models/MscaleModel'],
		function(Backbone, Mscale){
	
	var MscaleCollection = Backbone.Collection.extend({
		model: Mscale,
		url : "/api/v1/mscales/?format=json",
	
		parse: function(response) {
			this.recent_meta = response.meta || {};
			return response.objects || response;
		}
	});
	
	return MscaleCollection;
	
});




