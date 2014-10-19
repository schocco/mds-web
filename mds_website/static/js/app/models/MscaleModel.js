define(['models/BaseModel'],
		function(BaseModel){
	var Mscale = BaseModel.extend({
		
		prefix: "#/mscales/",
		urlRoot: "/api/v1/mscales/",
		
		/**
		 * returns true, when this is an intermediate step without a description.
		 */
		isPseudo: function(){
			return this.id % 1 != 0;
		}
	
	});
	return Mscale;
	
});


