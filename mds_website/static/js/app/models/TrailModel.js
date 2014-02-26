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
		 * @return the rating if present
		 */
		hasRating: function(){
			return this.get("udh_rating") != null || this.get("uxc_rating") != null
		},
		
		prefix: "#/trails/",
		urlRoot: "/api/v1/trails"
	
	});
	return Trail;
	
});


