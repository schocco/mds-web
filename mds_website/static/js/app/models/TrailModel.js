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
		
		validate: function(attributes, options){
			//TODO: validation logic
		},
		
		prefix: "#/trails/",
		urlRoot: "api/v1/trails"
	
	});
	return Trail;
	
});


