define(['backbone',
        'collections/TrailCollection',
        'underscore',
        'text!templates/trail_list.html',
        'jquery'],
		function(Backbone, TrailsCollection, _, tpl, $){
	
	var TrailsView = Backbone.View.extend({
		el: '#content',
		initialize: function () {
			var that = this;
		    var onDataHandler = function(collection) {
		    	console.log("fetched data.");
		        that.render();
		    }
		    that.collection = new TrailsCollection([]);
		    that.collection.fetch({ success : onDataHandler });
		    this.collection.on("reset", this.render, this);
		},
		render: function(){
			console.log("rendering");
			console.log(this.collection.models);
			var compiledTemplate = _.template( tpl, {'trails': this.collection.models });
			$(this.el).html(compiledTemplate);
			
		},
			
	});
	
	return TrailsView;
	
});


