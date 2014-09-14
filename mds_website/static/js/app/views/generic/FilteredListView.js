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
        'views/BaseView'
        ],
		function(Backbone, _, tpl, $, BaseView){
	
	var FilterView = Backbone.View.extend({
		
		searchFields: null,
		filters: null,
		pageSize: null,
		page: 1,
		totalPages: null,
		
		initialize: function (options) {
			this.readUrlParams();
			
			if(options){
				this.searchFields = options.searchFields;
				this.filters = options.filters;
				this.pageSize = options.pageSize;
				this.page = options.page;
				this.totalPages = options.totalPages;
			}
		    this.render();
		},
		
		/**
		 * Render pagination (if pagable),
		 * add filters (if present),
		 * add searchfields (if present)
		 */
		render: function() {
			var compiledTemplate = _.template(tpl, context);
			this.$el.html(compiledTemplate);
			this.addFilters();
			this.addSearchFields();
		},
		
		addFilters: function() {
			//TODO: iterate filters, create html and append
		},
		
		addSearchFields: function() {
			//TODO: iterate fields, create html and append it
		}
		
	});
	
	return HomeView;
	
});


