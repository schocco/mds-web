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
		
		/** retrieve the score for the current values without saving the object. */
		get_score: function(){
			//TODO: ajax request to get the calculated value for this object
			var score = {};
			return score;
		}
	
	});
	return UXC;
	
});


