define(['backbone', 'models/auth/SocialAuthBackend', 'collections/BaseCollection'],
		function(Backbone, SocialAuthBackend, BaseCollection){
	
	var BackendCollection = BaseCollection.extend({
		model: SocialAuthBackend,
		url : "/api/v1/socialauth_backends/"
	});
	
	return BackendCollection;
	
});




