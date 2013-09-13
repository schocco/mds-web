define(['models/BaseModel', 'underscore', 'jquery'],
		function(BaseModel, _, $){
	var UXC = BaseModel.extend({
		
		prefix: "#/uxc-scale/",
		urlRoot: "api/v1/uxc-scale",
		
		validate: function(attrs, options){
			errors = new Array();
			//total length must be a number
			if(!_.isNumber(parseFloat(attrs.total_length)) || isNaN(parseFloat(attrs.total_length))){
				errors[errors.length] = "Total length must be a numeric value, got " + attrs.total_length;
			}
			//difficulties must be a number, an object or a link but must not be empty
			var maxDiff = attrs.maximum_difficulty;
			if(_.isEmpty(maxDiff) || !($.isNumeric(maxDiff) || _.isString(maxDiff) || _.isObject(maxDiff)) ){
				errors[errors.length] = "Maximum difficulty must be set";
			}
			var avgDiff = attrs.maximum_difficulty;
			if(_.isEmpty(maxDiff) || !($.isNumeric(avgDiff) || _.isString(avgDiff) || _.isObject(avgDiff)) ){
				errors[errors.length] = "Average difficulty must be set";
			}
			//slope must be a number
			if(_.isEmpty(maxDiff) || !_.isNumber(parseFloat(attrs.total_length)) || isNaN(parseFloat(attrs.total_length))){
				errors[errors.length] = "Maximum slope (uphill) must be a number";
			}
			//total ascent must be a number
			if(_.isEmpty(maxDiff) || !_.isNumber(parseFloat(attrs.total_length)) || isNaN(parseFloat(attrs.total_length))){
				errors[errors.length] = "Total ascent must be a number";
			}
			if(errors.length > 0){
				return errors;
			}
		},
		
		/** retrieve the score for the current values without saving the object. */
		get_score: function(){
			var uri = this.urlRoot + "/calculate/";
			//TODO: ajax request to get the calculated value for this object
			var jqxhr = $.post(uri, this.attributes,
				function(data) {
					console.log("Success:");
					console.log(data);
				})
				.done(function() { console.log("second success"); })
				.fail(function(data) { console.log("error:" + data); })
				.always(function() { console.log("finished"); });
			var score = {};
			return score;
		}
	
	});
	return UXC;
	
});


