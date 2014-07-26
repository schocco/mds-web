define(['backbone',
        'underscore',
        'text!templates/auth/login_form.html',
        'jquery'
        ],
		function(Backbone, _, tpl, $){
	
	var LoginView = Backbone.View.extend({
		el: '#auth',
		
		
		initialize: function (options) {
			this.render();
		},

		
		/** renders the whole view. */
		render: function(){
			console.log("render auth modal");
			//var compiledTemplate = _.template( tpl, {'trail': this.trail });
			$(this.el).html(tpl);
			// add form submission handlers			
			
			$(this.el).modal();			
		}
			
	});
	
	return LoginView;
	
});


