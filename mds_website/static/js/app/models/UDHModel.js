define(['models/BaseModel', 'underscore', 'jquery'],
		function(BaseModel, _, $){
	var UDH = BaseModel.extend({

		prefix: "#/udh-scale/",
		urlRoot: "/api/v1/udh-scale",
		
		validate: function(attributes, options){
			//TODO: validation logic
		},
		
		/** retrieve the score for the current values without saving the object. */
		get_score: function(){
			var uri = this.urlRoot + "/calculate/";
			result = {};
			var that = this;
			var jqxhr = $.post(uri, this.attributes,
				function(data) { 
					that.score = data;
					console.log("Updated score for " + that);
					that.trigger("score_update");
				})
				.fail(function(data) {
					console.log("updating score for " + that + "failed");
					that.trigger("score_update", data);
					console.log(data);
				});
		},
		
		toString: function(){
			return "UDH Scale";
		}
	
	});
	return UDH;
	
});


