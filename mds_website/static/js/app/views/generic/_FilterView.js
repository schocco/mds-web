/**
 * Generic filter widget to display pagination options, search fields and
 * selects or checkboxes.
 * This is a nonfunctional view that only renders the data it is passed in as options.
 * 
 * Example:
 * 
 * searchFields = [{field:"name",label:"Name"}]
 * filters = [{field: type, choices: ["dh","uh"], label: "Type"}, {field: "owner", choices: [], label: "my uploads"}]
 * pageSize = 10
 * page = 1
 */
define(['backbone',
        'underscore',
        'text!templates/generic/_filterContainer.html',
        'text!templates/generic/_filterSearch.html',
        'text!templates/generic/_filterSelect.html',
        'text!templates/generic/_filterCheckbox.html',
        'jquery',
        'views/BaseView'
        ],
		function(Backbone, _, tpl, searchTpl, selectTpl, checkboxTpl, $, BaseView){
	
	var FilterView = Backbone.View.extend({
		
		searchFields: null,
		filters: null,
		pageSize: null,
		page: 1,
		totalPages: null,
		filterEl: "#filterFields",
		searchEl: "#searchFields",
		pagesEl: "#pageList",
		
		initialize: function (options) {
			this.readUrlParams();
			
			if(options){
				console.log(options);
				this.el = options.parent || this.el;
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
			var context = {};
			var compiledTemplate = _.template(tpl, context);
			this.$el.html(compiledTemplate);
			this.addFilters();
			this.addSearchFields();
			this.addPages();
		},
		
		readUrlParams: function(){
			//TODO
		},
		
		addFilters: function() {
			//clear element
			var $filterEl = $(this.filterEl);
			$filterEl.html("");
			//templates
			_.each(this.filters, function(filter, key, list){
				var rendered = "";
				if(filter.choices.length == 1){
					//render checkbox element
					rendered = _.template(checkboxTpl, {filter: filter});
				} else if(filter.choices.length > 1){
					// render select element with all choices
					rendered = _.template(selectTpl, {filter: filter});
				}
				$filterEl.append(rendered);
			});
			return this;
		},
		
		addSearchFields: function() {
			if(this.searchFields && this.searchFields.length >= 1){
				var rendered = _.template(searchTpl, {fields: this.searchFields});
				$(this.searchEl).html(rendered);
			}
			return this;
		},
		
		addPages: function() {
			$(this.pagesEl).html('<p>Page 1 of 2 | <a href="" class="label icon-arrow-left"></a> <a href="" class="label">1</a> <a href="#" class="label">2</a> <a href="" class="label icon-arrow-right"></a></p>');
		},
		
		addSorting: function() {
			
		},
		
	});
	
	return FilterView;
	
});


