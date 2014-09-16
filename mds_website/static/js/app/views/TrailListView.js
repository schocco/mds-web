define(['backbone',
        'collections/TrailCollection',
        'cache',
        'underscore',
        'views/BaseView',
        'views/generic/_FilterView',
        'views/generic/FilteredListView',
        'text!templates/trail_list.html',
        'jquery',
        ],
		function(Backbone, TrailsCollection, cache, _, BaseView, FilterView, tpl, $){
	
	var TrailsView = BaseView.extend({
		el: '#content',
		title: "Trails",
		filterOptions: {
			el: "#filters",
			searchFields: [{field: "name"},{field: "length"}],
			filters: [{field: "type", choices: [["downhill","downhill"],["uh","uphill"]], label: "type"},
			          {field: "owner", choices: ["rocco"], label: "uploaded by me"},
			          {field: "type", choices: ["downhill"], label: "downhill"},
			          {field: "type", choices: ["xc"], label: "cross country"}],
			sorting: [["name", "name"], ["length","length"]]
		},
		
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
		
		applyFilters: function(e){
			e.preventDefault();
			var filters = this.filterView.getFilters();
			var sorting = this.filterView.getSorting();
			this.collection
			.setFilterOptions(filters)
			.setSorting(sorting.field)
			.setSortOrder(sorting.order)
			.getFirstPage();
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
			this.filterView = new FilterView(this.filterOptions, {el:"#filters"});
			
			this.listView = new FilteredListView({collection: this.collection});
			
			_.bindAll(this, "loadNextPage", "loadPrevPage", "applyFilters");
			$('#nextPage').click(this.loadNextPage);
			$('#prevPage').click(this.loadPrevPage);
			$('#applyFilters').click(this.applyFilters);
		},
		
		renderList: function(){
			if(this.listView){
				this.listView.render();
			}
			//var compiledTemplate = _.template( tpl, {'trails': this.collection });
		}
			
	});
	
	return TrailsView;
	
});


