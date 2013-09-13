define(['models/BaseModel'],
		function(BaseModel){
	var UXC = BaseModel.extend({
		
		prefix: "#/uxc-scale/",
		urlRoot: "api/v1/uxc-scale",
		
		validate: function(attributes, options){
			//TODO: validation logic
		},
		
		/** retrieve the score for the current values without saving the object. */
		get_score: function(){
			//TODO: ajax request to get the calculated value for this object
			var score = {};
			return score;
		}
	
	});
	return UXC;
	
});


