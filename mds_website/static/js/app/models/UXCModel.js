define(['models/ScaleBaseModel', 'underscore', 'jquery'],
		function(ScaleBaseModel, _, $){
	var UXC = ScaleBaseModel.extend({
		
		prefix: "#/uxc-scale/",
		urlRoot: "/api/v1/uxc-scale/",
		
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
			if(_.isEmpty(attrs.maximum_slope_uh) || !_.isNumber(parseFloat(attrs.maximum_slope_uh)) || isNaN(parseFloat(attrs.maximum_slope_uh))){
				errors[errors.length] = "Maximum slope (uphill) must be a number";
			}
			//total ascent must be a number
			if(_.isEmpty(attrs.total_ascent) || !_.isNumber(parseFloat(attrs.total_ascent)) || isNaN(parseFloat(attrs.total_ascent))){
				errors[errors.length] = "Total ascent must be a number";
			}
			if(errors.length > 0){
				return errors;
			}
		},
		
		
		toString: function(){
			return "UXC Scale";
		}
		
		
	});
	return UXC;
	
});


