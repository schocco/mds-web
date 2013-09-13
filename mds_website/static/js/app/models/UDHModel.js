define(['models/BaseModel'],
		function(BaseModel){
	var UDH = BaseModel.extend({

		prefix: "#/udh-scale/",
		urlRoot: "api/v1/udh-scale",
		
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
	return UDH;
	
});


