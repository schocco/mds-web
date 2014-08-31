define(['backbone',
        'underscore',
        'text!templates/auth/auth.html',
        'jquery',
        'views/auth/LoginView'
        ],
		function(Backbone, _, tpl, $, LoginView){
	
	var AuthView = Backbone.View.extend({
		el: '#auth',
		
		
		initialize: function (options) {
			this.render();
		},

		
		/** renders the whole view. */
		render: function(){
			console.log("render auth view");
			var compiledTemplate = _.template( tpl, {'user': 'rocco' });
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


