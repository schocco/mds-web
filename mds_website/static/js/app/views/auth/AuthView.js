define(['backbone',
        'underscore',
        'text!templates/auth/auth.html',
        'jquery',
        'views/auth/LoginView',
        'collections/auth/UserCollection',
        'models/auth/UserModel'
        ],
		function(Backbone, _, tpl, $, LoginView, UserCollection, UserModel){
	
	/**
	 * The view initially checks if the user is logged in and either renders a login or a logout button accordingly.
	 * If the authentication status changes (events of UserModel), then the view is re-rendered.
	 */
	var AuthView = Backbone.View.extend({
		el: '#auth',
		loggedIn: false,
		user: null,
		
		initialize: function (options) {
			var that = this;
			
		    var userHandler = function(collection){
		    	that.user = collection.pop();
		    	UserModel.c
		    	that.loggedIn = true;
		    	that.render();
		    };
		    var errHandler = function(collection, resp, options){
		    	if(resp.status == 401){
		    		that.loggedIn = false;
		    		that.user = null;
		    	}
		    	that.render();
		    };
		    var loggedInHandler = function(){
		    	var users = new UserCollection().fetch({success: userHandler, error: errHandler});
		    };
		    var loggedOutHandler = function(){
		    	console.log("logouthandler");
		    	that.loggedIn = false;
		    	that.user = null;
		    	that.render();
		    }
		    
		    //this.loggedIn = UserModel.isAuthenticated({loggedIn: loggedInHandler, loggedOut: loggedOutHandler});
		    this.user = UserModel.currentUser;
		   // this.loggedIn = user.isAuthenticated();
		    this.render();
			UserModel.events.on("user_login", loggedInHandler, this);
			UserModel.events.on("user_logout", loggedOutHandler, this);
		},

		
		/** renders the whole view. */
		render: function(){
			var compiledTemplate = _.template( tpl, {'user': this.user, 'loggedIn': this.loggedIn });
			$(this.el).html(compiledTemplate);
			var that = this;
			// connect links
			$("#loginLink").click(function(event){
				event.preventDefault();
				$(this).hide();
				var view = new LoginView();
			});
			$('#logoutLink').click(function(event){
				event.preventDefault();
				that.logout();
			});
		},
		
		logout: function(){
			UserModel.logout();			
		}
			
	});
	
	return AuthView;
	
});


