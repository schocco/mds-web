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
		
		/**
		 * @return boolean
		 */
		hasRatings: function(){
			return this.get("udh_ratings").length > 0 || this.get("uxc_ratings").length > 0
		},
		
		prefix: "#/trails/",
		urlRoot: "api/v1/trails"
	
	});
	return Trail;
	
});


