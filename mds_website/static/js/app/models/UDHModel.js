define(['models/BaseModel'],
		function(BaseModel){
	var UXC = BaseModel.extend({
		
		defaults: {
			"name":  "unnamed",
			"type":	 "unknown",
			"description": "-",
		},
		prefix: "#/uxc/",
		urlRoot: "api/v1/uxc",
	
	});
	return UXC;
	
});


