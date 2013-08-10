define(['models/BaseModel'],
		function(BaseModel){
	var Trail = BaseModel.extend({
		defaults: {
			"name":  "unnamed",
			"description": "-",
		},
		prefix: "#/trails/",
		urlRoot: "api/v1/trails",
	
	});
	return Trail;
	
});


