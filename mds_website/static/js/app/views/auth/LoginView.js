define(['backbone',
        'underscore',
        'cache',
        'text!templates/auth/login_form.html',
        'jquery',
        'collections/auth/SocialAuthBackendCollection',
        'collections/auth/UserCollection'
        ],
		function(Backbone, _, cache, tpl, $, SocialAuthBackendCollection, UserCollection){
	
	var LoginView = Backbone.View.extend({
		el: '#authSub',
		
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
				$('#loginForm').submit();
			});
		}
			
	});
	
	return LoginView;
	
});


