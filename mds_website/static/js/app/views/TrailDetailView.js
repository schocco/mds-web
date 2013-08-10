define(['backbone',
        'models/TrailModel',
        'underscore',
        'text!templates/trail_detail.html',
        'jquery'],
		function(Backbone, Trail, _, tpl, $){
	
	var TrailDetailView = Backbone.View.extend({
		el: '#content',
		initialize: function (options) {
			var that = this;
		    var onDataHandler = function(model) {
		    	console.log("fetched trail");
		        that.render();
		    }
		    that.id = options.id;
		    that.trail = new Trail({id: that.id});
		    that.trail.fetch({success: onDataHandler});
		    //that.trail.on("reset", this.render, this);
		},
		
		render: function(){
			console.log("render template");
			var compiledTemplate = _.template( tpl, {'trail': this.trail });
			$(this.el).html(compiledTemplate);
			
		},
			
	});
	
	return TrailDetailView;
	
});


