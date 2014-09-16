define(['backbone',
        'collections/TrailCollection',
        'cache',
        'underscore',
        'views/BaseView',
        'views/generic/FilteredListView',
        'text!templates/trails.html',
        'text!templates/trail_item.html',
        'jquery',
        ],
		function(Backbone, TrailsCollection, cache, _, BaseView, FilteredListView, tpl, itemTpl, $){
	
	var TrailsView = BaseView.extend({
		
		title: "Trails",
		
		initialize: function () {
			BaseView.prototype.initialize.apply(this);
			var that = this;
		    var onDataHandler = function(collection) {
		        that.render();
		    }
		    this.collection = cache.get('TrailsCollection', TrailsCollection, { success : onDataHandler });
		    if(this.collection.length){
		    	this.render();
		    }
		    
		},
		
		render: function(){
			
			var options = {
					el: "#content",
					collection: this.collection,
					template: tpl,
					itemTemplate: itemTpl,
				};
			this.listView = new FilteredListView(options);	
			
		},
			
	});
	
	return TrailsView;
	
});


