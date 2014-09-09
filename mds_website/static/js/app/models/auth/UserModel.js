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
		
		/** Authenticates the user.
		 * @param success callback function
		 * @param error callback function
		 * */
		login: function(options){
			var uri = this.urlRoot + "login/";
			var that = this;
			var loginData = {username: that.get("username"), password: that.get("password")};
			$.ajax(uri, {
					data: JSON.stringify(loginData),
					type: "POST",
					contentType:"application/json; charset=utf-8"
				})
				.done(function(data) {
					//TODO: set user data
					console.log("user logged in");
					console.log(data);
					that.trigger("user_login");
					if(options.success){
						options.success(data.responseJSON);
					}
				})
				.fail(function(data) {
					console.log("login failed");
					that.trigger("user_login_failed", data.responseJSON);
					if(options.error){
						options.error(data.responseJSON);
					}
				});
		},
		
		/** Terminates the session. */
		logout: function(){
			var uri = this.urlRoot + "calculate/";
			result = {};
			var that = this;
			var jqxhr = $.post(uri, this.attributes,
				function(data) { 
					that.set("score", data);
					console.log("Updated score for " + that);
					that.trigger("score_update");
				})
				.fail(function(data) {
					console.log("updating score for " + that + "failed");
					that.trigger("score_update", data);
					console.log(data);
				});
		}
	
	},
	/* static methods */
	{
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
		}
	});
	
	return UserModel;
	
});


