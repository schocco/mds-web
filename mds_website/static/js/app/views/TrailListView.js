define(['backbone',
        'collections/TrailCollection',
        'cache',
        'underscore',
        'views/BaseView',
        'text!templates/trail_list.html',
        'jquery',
        ],
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
		
		loadNextPage: function(e){
			e.preventDefault();
			console.log("getting next page");
			this.collection.getNextPage();
		},
		
		loadPrevPage: function(e){
			e.preventDefault();
			console.log("getting prev page");
			this.collection.getPreviousPage();
		},
		
		render: function(){
			var compiledTemplate = _.template( tpl, {'trails': this.collection });
			this.setContent(compiledTemplate);
			_.bindAll(this, "loadNextPage", "loadPrevPage");
			$('#nextPage').click(this.loadNextPage);
			$('#prevPage').click(this.loadPrevPage);
			
		},
			
	});
	
	return TrailsView;
	
});


