define(['backbone',
        'underscore',
        'text!templates/auth/auth.html',
        'jquery',
        'views/auth/LoginView',
        'collections/auth/UserCollection',
        'models/auth/UserModel'
        ],
		function(Backbone, _, tpl, $, LoginView, UserCollection, UserModel){
	
	var AuthView = Backbone.View.extend({
		el: '#auth',
		loggedIn: false,
		user: null,
		
		initialize: function (options) {
			var that = this;
			
		    var userHandler = function(collection){
		    	that.user = collection.pop();
		    	loggedIn: true;
		    	that.render();
		    };
		    var errHandler = function(collection, resp, options){
		    	if(resp.status == 401){
		    		loggedIn: false;
		    	}
		    	that.render();
		    };
		    var loggedInHandler = function(){
		    	var users = new UserCollection().fetch({success: userHandler, error: errHandler});
		    };
		    var loggedOutHandler = function(){
		    	loggedIn: false;
		    	that.render();
		    }
		    
		    UserModel.isAuthenticated({loggedIn: loggedInHandler, loggedOut: loggedOutHandler});
		},

		
		/** renders the whole view. */
		render: function(){
			var compiledTemplate = _.template( tpl, {'user': this.user });
			$(this.el).html(compiledTemplate);

			// connect links
			$("#loginLink").click(function(event){
				event.preventDefault();
				var view = new LoginView();
			});			
		}
			
	});
	
	return AuthView;
	
});


