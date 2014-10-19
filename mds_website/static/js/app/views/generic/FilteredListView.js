/**
 * Generic ListView for backbone collections that provide 
 * filtering and pagination functionality.
 * 
 */
define(['backbone',
        'underscore',
        'text!templates/home.html',
        'jquery',
        'views/BaseView',
        'views/generic/_FilterView',
        ],
        function(Backbone, _, tpl, $, BaseView, FilterView){

	var FilteredListView = BaseView.extend({

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
		 * 										dom element with id=filters and an element with the id=items.
		 * 										Elements with the class "pageList" will be filled with links for
		 * 										navigation between pages.
		 * @param {String} options.itemTemplate	Template for a single list item.
		 * @param {object} options.context		Context object for template rendering (available in both templates)
		 * @param {boolean} options.filtered 	Whether or not the filter-box should be displayed
		 * @param {int} options.pageSize 		number of elements per page
		 */
		initialize: function (options) {
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
		    };
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
			this.setContent(compiledTemplate);
			if(this.filtered){
				this.addFilters();
			}
			this.addItems();
			_.bindAll(this, "loadNextPage", "loadPrevPage", "applyFilters", "resetFilters");
			$('#applyFilters').click(this.applyFilters);
			$('#resetFilters').click(this.resetFilters);
		},
		
		addItems: function(items, response){
			//also need to update the paging stuff
			var pageInfo = {
					total: this.collection.getTotalPages(),
					current: this.collection.currentPageNumber()
			};
			this.filterView.updatePages(pageInfo);
			_.bindAll(this, "loadPage", "loadNextPage", "loadPrevPage");
			$('.pageLink').click(this.loadPage);
			$('.nextPage').click(this.loadNextPage);
			$('.prevPage').click(this.loadPrevPage);
			
			console.log("adding items");
			var itemEl;
			var itemContainer = $('#items');
			itemContainer.html("");
			itemContainer.hide();
			
			console.log("pages:");
			
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
		
		/**
		 * @description
		 * Re-renders the filter view to reset all elements
		 * and removes the current settings from the collection.
		 */
		resetFilters: function(e){
			e.preventDefault();
			this.addFilters()
			this.collection.clearSettings();
			this.collection.getFirstPage();
		},
		
		loadNextPage: function(e){
			e.preventDefault();
			this.collection.getNextPage();
		},
		
		loadPrevPage: function(e){
			e.preventDefault();
			this.collection.getPreviousPage();
		},
		
		loadPage: function(e){
			e.preventDefault();
			var page = parseInt($(e.target).attr("href").substring(1));
			this.collection.getPage(page);
		}

	});

	return FilteredListView;

});


