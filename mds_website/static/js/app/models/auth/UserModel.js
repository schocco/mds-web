define(['models/BaseModel'],
		function(BaseModel){
	var urlRoot = "/api/v1/user/";
	var UserModel = BaseModel.extend({
		
		prefix: "",
		urlRoot: "/api/v1/user/",
		defaults: {
			username: "anonymous",
			password: "",
		},
		
		get_url: function(){
			return this.prefix + this.get('name') + "/";
		},
		
		
	
	},
	/* static methods */
	{
		
		/** field which is used to trigger events. */
		events: _.extend({}, Backbone.Events),
		
		/** Checks if the current user is logged in by sending a request to the server.
		 * If no sessionid cookie is sent or the session has expired, the user is not logged in.
		 * 
		 * @param loggedIn	 a function that is called when the user is logged in
		 * @param loggedOut	 a function that is called when the user is logged out
		 * @param error		 a function that is called when an error occurs
		 * */
		isAuthenticated: function(options){
			//var urlRoot = "/api/v1/user/"
			var uri = urlRoot + "auth-status/";
			var that = this;
			var jqxhr = $.get(uri, this.attributes,
				function(data) { 
					if(data.status == "loggedin"){
						console.log("logged in, data:");
						console.log(data);
						if(options.loggedIn){options.loggedIn(data);}						
					} else {
						console.log("not logged in, data:");
						if(options.loggedOut){options.loggedOut(data);}
					}
				})
				.fail(function(data) {
					if(options.error){options.error(data);}
				});
		},
		
		/** Terminates the session. */
		logout: function(){
			
			var uri = urlRoot + "logout/";
			var that = this;
			$.getJSON(uri).done(
				function(data) {
					console.log("logged out");
					that.events.trigger("user_logout");
				})
				.fail(function(data) {
					console.log("logout error");
					console.log(data);
				});
		},
		
		/** Authenticates the user.
		 * @param username
		 * @param password
		 * @param options with keys: 
		 * 		success (callback function) & 
		 * 		error (callback function)
		 * */
		login: function(username, password, options){
			var uri = urlRoot + "login/";
			var that = this;
			var loginData = {username: username, password: password};
			$.ajax(uri, {
					data: JSON.stringify(loginData),
					type: "POST",
					contentType:"application/json; charset=utf-8"
				})
				.done(function(data) {
					that.events.trigger("user_login");
					if(options.success){
						options.success(data.responseJSON);
					}
				})
				.fail(function(data) {
					that.events.trigger("user_login_failed", data.responseJSON);
					if(options.error){
						options.error(data.responseJSON);
					}
				});
		},
		

		
	});
	
	return UserModel;
	
});

