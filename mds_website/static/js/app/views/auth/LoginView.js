define(['backbone',
        'underscore',
        'cache',
        'text!templates/auth/login_form.html',
        'jquery',
        'collections/auth/SocialAuthBackendCollection',
        'collections/auth/UserCollection',
        'models/auth/UserModel',
        'views/util/MessageMixin'
        ],
		function(Backbone, _, cache, tpl, $, SocialAuthBackendCollection, UserCollection, UserModel, MessageMixin){
	
	var LoginView = Backbone.View.extend({
		el: '#authSub',
		msg: '#login_msg',
		
		initialize: function (options) {
			//TODO: try to force HTTPS
			//get collection with available auth backends
			var that = this;
		    var onDataHandler = function(collection) {
		    	console.log("collection received.");
		    	console.log(that.collection);
		        that.render();
		    };
		    var userHandler = function(coll){
		    	that.user = coll.pop();
		    	console.log("user: " + that.user.get("username"));
		    };
		    //var users = new UserCollection().fetch({async:false, reset: true, success: userHandler});
		    this.collection = cache.get('SocialAuthBackendCollection', SocialAuthBackendCollection, { success : onDataHandler });
		    this.collection.on("reset", this.render, this);

		},
		
		clearForm: function(){
			$('#id_username').val("");
			$('#id_password').val("");
			this.hideMessage()
		},
		

		
		/** renders the whole view. */
		render: function(){
			console.log("render login view");
			var that = this;
			
			var compiledTemplate = _.template(tpl)({'backends': this.collection.models });
			$(this.el).html(compiledTemplate);
			$('#loginSubmit').click(function(e){
				e.preventDefault();
				console.log("login clicked.");
				var username = $('#id_username').val();
				var password = $('#id_password').val();
				
				var success = function(data){
					that.clearForm();
					that.showMessage({type:MessageMixin.INFO, message: "you are now logged in"});
				}
				var err = function(data){
					that.clearForm();
					var message = "Login failed. Username or password were not correct.";
					if(data.reason == "disabled"){
						message = "Your account has been disabled. Please contact the administrator.";
					}
					that.showMessage({type:MessageMixin.ERROR, msg: message});
				}
				UserModel.login(username, password, {success:success, error:err});
			});
		}
			
	});
	
	return LoginView;
	
});


