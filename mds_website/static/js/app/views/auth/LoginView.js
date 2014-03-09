define(['backbone',
        'underscore',
        'text!templates/auth/login.html',
        'jquery'
        ],
		function(Backbone, _, tpl, $){
	
	var LoginView = Backbone.View.extend({
		el: '#auth',
		
		
		initialize: function (options) {
			var that = this;
		},

		
		/** renders the whole view. */
		render: function(){
			console.log("render auth modal");
			var compiledTemplate = _.template( tpl, {'trail': this.trail });
			$(this.el).html(compiledTemplate);
			
			console.log("create hight profile");
			this.render_height_profile();
			
			console.log("create map.");
			this.render_map();
			
			console.log("create score/rating view");
			this.render_score();
			
			// add handler to link
			var that = this;
			$('#rate').click(function(event){
				event.preventDefault();
				var rateview = new TrailRatingView({trail: that.trail});
			});
		}
			
	});
	
	return LoginView;
	
});


