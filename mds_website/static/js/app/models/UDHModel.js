define(['models/ScaleBaseModel', 'underscore', 'jquery'],
		function(ScaleBaseModel, _, $){
	var UDH = ScaleBaseModel.extend({

		prefix: "#/udh-scale/",
		urlRoot: "/api/v1/udh-scale",
		
		validate: function(attributes, options){
			//TODO: validation logic
		},
		
		toString: function(){
			return "UDH Scale";
		}
	
	});
	return UDH;
	
});


