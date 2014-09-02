define(['backbone',
        'cache',
        'underscore',
        'text!templates/home.html',
        'jquery'
        ],
		function(Backbone, cache, _, tpl, $){
	
	var HomeView = Backbone.View.extend({
		el: '#content',
		initialize: function () {
			var that = this;
			//TODO: change #header
		    this.render();
		    
		},
		render: function(){
			console.log("rendering home view");
			var compiledTemplate = _.template( tpl, {'meta': {} });
			
			
			$(this.el).fadeOut(function() {
				  $(this).html(compiledTemplate).fadeIn();
			});
			
		},
		
			
	});
	
	return HomeView;
	
});


