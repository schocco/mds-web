define(['backbone'],
		function(Backbone){
	var Trail = Backbone.Model.extend({
		defaults: {
			"name":  "unnamed",
			"description": "-",
		}
	});
	return Trail;
	
});


