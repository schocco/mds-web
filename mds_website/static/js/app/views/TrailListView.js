define(['backbone',
        'collections/TrailCollection',
        'cache',
        'underscore',
        'text!templates/trail_list.html',
        'jquery',
        'chart'],
		function(Backbone, TrailsCollection, cache, _, tpl, $){
	
	var TrailsView = Backbone.View.extend({
		el: '#content',
		initialize: function () {
			var that = this;
		    var onDataHandler = function(collection) {
		    	console.log("fetched data.");
		        that.render();
		    }
		    this.collection = cache.get('TrailsCollection', TrailsCollection, { success : onDataHandler });
		    this.collection.on("reset", this.render, this);
		    if(this.collection.length){
		    	this.render();
		    }
		    
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


