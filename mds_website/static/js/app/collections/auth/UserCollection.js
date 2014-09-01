define(['backbone', 'models/auth/UserModel', 'collections/BaseCollection'],
		function(Backbone, UserModel, BaseCollection){
	
	var UserCollection = BaseCollection.extend({
		model: UserModel,
		url : "/api/v1/user/"
	
	});
	
	return UserCollection;
	
});




