define(['backbone'],
		function(Backbone){
	var BaseModel = Backbone.Model.extend({
		
		prefix: "#/",
		
		get_url: function(){
			return this.prefix + this.get('id');
		}
	
	});
	return BaseModel;
	
});


