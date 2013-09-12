define(['models/BaseModel'],
		function(BaseModel){
	var UDH = BaseModel.extend({
		
		defaults: {
			"name":  "unnamed",
			"type":	 "unknown",
			"description": "-",
		},
		prefix: "#/udh/",
		urlRoot: "api/v1/udh",
	
	});
	return UDH;
	
});


