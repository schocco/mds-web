define(['models/BaseModel'],
		function(BaseModel){
	var Mscale = BaseModel.extend({
		
		prefix: "#/mscales/",
		urlRoot: "/api/v1/mscales",
	
	});
	return Mscale;
	
});


