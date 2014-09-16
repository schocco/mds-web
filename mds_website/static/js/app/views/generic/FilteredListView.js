/**
 * Generic view to render any collection with a bar for filtering and pagination.
 */
/**
 * Generic filter bar to display pagination options, search fields and
 * selects or checkboxes.
 * This is a nonfunctional view that only renders the data it is passed in as options.
 * 
 * Requires a pageable collection
 * 
 * Example
 * searchableFields = ["name"]
 * filters = [{field: type, choices: ["dh","uh"], label: "Type"}, {field: "owner", choices: [], label: "my uploads"}]
 * pageSize = 10
 * page = 1
 */
define(['backbone',
        'underscore',
        'text!templates/home.html',
        'jquery',
        'views/BaseView',
        'views/generic/_FilterView',
        ],
        function(Backbone, _, tpl, $, BaseView, FilterView){

	var FilteredListView = Backbone.View.extend({

		searchFields: null,
		filters: null,
		pageSize: null,
		page: 1,
		totalPages: null,
		filtered: true,


		/**
		 * @description
		 * Creates a new generic (filtered & paginated) listview with the provided
		 * collection and templates.
		 *
		 * @param {Object} options 				The options object
		 * @param {Object} options.collection 	An already fetched BaseCollection with
		 * 										pagination support
		 * @param {String} options.template 	The template string for rendering 
		 * 										with underscore. The template must contain a 
		 * 										dom element with id=filters and an element with the id=items
		 * @param {String} options.itemTemplate	Template for a single list item
		 * @param (object} options.context		Context object for template rendering
		 * @param {boolean} options.filtered 	Whether or not the filter-box should be displayed
		 * @param {int} options.pageSize 		number of elements per page
		 */
		initialize: function (options) {
			
			//TODO: read url params to preset filters before fetching collection
			if(options){
				if(options.filtered !== undefined){
					this.filtered = options.filtered;
				}
				this.context = options.context || {};
				this.collection = options.collection;
				this.template = options.template;
				this.itemTemplate = options.itemTemplate;
				this.pageSize = options.pageSize;
				this.el = options.el;
			} else {
				throw "MissingArgument: options object is required";
			}
			this.searchFields = this.collection.searchFields;
			this.filters = this.collection.filters;
			this.sortFields = this.collection.sortFields;
			this.totalPages = this.collection.getTotalPages();

			
			var that = this;
		    var onDataHandler = function(collection) {
		        that.render();
		    }
		    this.collection.on("reset", this.addItems, this);
		    this.render();
		},

		/**
		 * @description
		 * Renders pagination, searchfields and filters (if present) via subview,
		 * clears this.$el and appends all items to this.$el
		 */
		render: function() {
			var compiledTemplate = _.template(this.template, _.extend(this.context, {items: this.collection}));
			this.$el.html(compiledTemplate);
			if(this.filtered){
				this.addFilters();
			}
			this.addItems();
			_.bindAll(this, "loadNextPage", "loadPrevPage", "applyFilters");
			$('#nextPage').click(this.loadNextPage);
			$('#prevPage').click(this.loadPrevPage);
			$('#applyFilters').click(this.applyFilters);
		},
		
		addItems: function(items, response){
			console.log("adding items");
			var itemEl;
			var itemContainer = $('#items');
			itemContainer.html("");
			itemContainer.hide();
			
			this.collection.each(function(item){
				itemEl = _.template(this.itemTemplate, {item: item});
				itemContainer.append(itemEl);
			}, this);
			itemContainer.fadeIn();
		},

		addFilters: function() {
			// create _FilterView with data from the collection
			console.log("add filters");
			var filterOptions = {
					el: "#filters",
					searchFields: this.searchFields,
					filters: this.filters,
					sorting: this.sortFields,
			};
			this.filterView = new FilterView(filterOptions);
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

	});

	return FilteredListView;

});


