define(['backbone',
        'collections/TrailCollection',
        'cache',
        'underscore',
        'views/BaseView',
        'text!templates/trail_list.html',
        'jquery',
        'chart'],
		function(Backbone, TrailsCollection, cache, _, BaseView, tpl, $){
	
	var TrailsView = BaseView.extend({
		el: '#content',
		title: "Trails",
		
		initialize: function () {
			BaseView.prototype.initialize.apply(this);
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
			this.setContent(compiledTemplate);
			
		},
			
	});
	
	return TrailsView;
	
});


