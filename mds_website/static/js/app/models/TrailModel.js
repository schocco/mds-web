define(['models/BaseModel'],
		function(BaseModel){
	var Trail = BaseModel.extend({
		// types allowed
		type_choices : {
			"unknown": "unknown",
			"downhill": "downhill",
			"uphill": "uphill",
			"xc": "cross country"
		},
		
		defaults: {
			"name":  "unnamed",
			"type":	 "unknown",
			"description": "-",
		},
		prefix: "#/trails/",
		urlRoot: "api/v1/trails",
	
	});
	return Trail;
	
});


