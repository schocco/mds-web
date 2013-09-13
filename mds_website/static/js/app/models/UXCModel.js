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
		
		/** retrieve the score for the current values without saving the object. */
		get_score: function(){
			//TODO: ajax request to get the calculated value for this object
			var score = {};
			return score;
		}
	
	});
	return UDH;
	
});


