define(['backbone',
        'underscore',
        'text!templates/auth/login_form.html',
        'jquery'
        ],
		function(Backbone, _, tpl, $){
	
	var LoginView = Backbone.View.extend({
		el: '#authSub',
		
		initialize: function (options) {
			//TODO: try to force HTTPS
			this.render();
		},

		
		/** renders the whole view. */
		render: function(){
			console.log("render login view");
			var that = this;
			$(this.el).html(tpl);
			$('#loginSubmit').click(function(e){
				e.preventDefault();
				console.log("login clicked.");
				$('#loginForm').submit();
			});
		}
			
	});
	
	return LoginView;
	
});


