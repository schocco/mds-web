define(['models/BaseModel'],
		function(BaseModel){
	var UserModel = BaseModel.extend({
		
		prefix: "",
		urlRoot: "/api/v1/user/",
		
		get_url: function(){
			return this.prefix + this.get('name') + "/";
		}
	
	});
	return UserModel;
	
});


