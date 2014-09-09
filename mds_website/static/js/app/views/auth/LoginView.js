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
		    if(this.collection.length){
				this.render(); //needed when collection loaded from cache
		    }

		},
		

		
		/** renders the whole view. */
		render: function(){
			console.log("render login view");
			var that = this;
			
			var compiledTemplate = _.template( tpl, {'backends': this.collection.models });
			$(this.el).html(compiledTemplate);
			$('#loginSubmit').click(function(e){
				e.preventDefault();
				console.log("login clicked.");
				//TODO: get username and password
				var username = $('#id_username').val();
				var password = $('#id_password').val();
				//create user object
				var user = new UserModel({username:username,password:password}); //{username:username,password:password}
				var success = function(data){
					that.hideMessage();
					that.showMessage({type:MessageMixin.INFO, message: "you are now logged in"});
				}
				var err = function(data){
					that.hideMessage();
					var message = "Login failed. Username or password were not correct.";
					if(data.reason == "disabled"){
						message = "Your account has been disabled. Please contact the administrator.";
					}
					that.showMessage({type:MessageMixin.ERROR, msg: message});
				}
				user.login({success:success, error:err});
				//cache user
			});
		}
			
	});
	
	return LoginView;
	
});


