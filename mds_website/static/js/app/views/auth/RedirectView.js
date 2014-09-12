define(['backbone',
        'underscore',
        'text!templates/auth/redirect.html',
        'jquery',
        'models/auth/UserModel',
        'views/BaseView',
        'views/util/MessageMixin',
        ],
		function(Backbone, _, tpl, $, UserModel, BaseView, MessageMixin){
	
	/**
	 * Notify the user that they must be logged in in order to see the requested contents.
	 * Forward to the url that is given in the options if a login event occurs.
	 */
	var RedirectView = BaseView.extend({
		loggedIn: false,
		msg: "#redirectMsg",
		
		initialize: function (options) {
			this.render();
		},

		
		/** renders the whole view. */
		render: function(){
			var compiledTemplate = _.template( tpl, {'user': this.user });
			this.setContent(compiledTemplate);
			this.showMessage({
				msg: "You are not authorized. Please log in below to proceed.",
				type: MessageMixin.ERROR
			});
		}
			
	});
	
	return RedirectView;
	
});


