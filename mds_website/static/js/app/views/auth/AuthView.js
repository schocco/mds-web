define(['backbone',
        'underscore',
        'text!templates/auth/auth.html',
        'jquery',
        'views/auth/LoginView',
        'collections/auth/UserCollection'
        ],
		function(Backbone, _, tpl, $, LoginView, UserCollection){
	
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
		    	that.render();
		    	}
		    };
		    var users = new UserCollection().fetch({success: userHandler, error: errHandler});
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


