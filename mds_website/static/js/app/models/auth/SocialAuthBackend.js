define(['models/BaseModel'],
		function(BaseModel){
	var SocialAuthBackend = BaseModel.extend({
		
		prefix: "/login/",
		urlRoot: "/api/v1/socialauth_backends/",
		
		get_url: function(){
			return this.prefix + this.get('name') + "/";
		}
	
	});
	return SocialAuthBackend;
	
});


