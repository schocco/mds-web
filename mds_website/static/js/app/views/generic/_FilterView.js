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
        'text!templates/generic/_filterSort.html',
        'text!templates/generic/_filterPaging.html',
        'jquery',
        'views/BaseView'
        ],
		function(Backbone, _, tpl, searchTpl, selectTpl, checkboxTpl, sortTpl, pageTpl, $, BaseView){
	
	var FilterView = Backbone.View.extend({
		
		searchFields: null,
		filters: null,
		sorting: null,
		pageSize: null,
		page: 1,
		totalPages: null,
		filterEl: "#filterFields",
		searchEl: "#searchFields",
		pagesEl: "#pageList",
		sortingEl: "#sortFields",
		
		initialize: function (options) {
			this.readUrlParams();
			
			if(options){
				console.log(options);
				this.el = options.parent || this.el;
				this.searchFields = options.searchFields;
				this.filters = options.filters;
				this.sortFields = options.sorting;
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
			this.addSorting();
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
		
		updatePages: function(pageInfo){
			var pages = _.range(1, pageInfo.total+1);
			var context = {
					pages: pages,
					current: pageInfo.current || 1, 
					total: pageInfo.total
					};
			var compiled = _.template(pageTpl, context);
			$(this.pagesEl).html(compiled);
		},
		
		addSorting: function() {
			var sort = _.template(sortTpl, {fields: this.sortFields});
			$(this.sortingEl).append(sort);
		},
		
		/**
		 * Reads sorting information
		 */
		getSorting: function() {
			var sortField = $("#filterOrderField").val();
			var sortOrder = $("#filterOrder").val();
			return {field: sortField, order: sortOrder};
		},
		
		/**
		 * Returns a list of objects. Each object represents one filter and has the
		 * attributes name and value.
		 */
		getFilters: function(){
			console.log("read filter vals");
			var filters = {};
			$(this.filterEl + " input[type=checkbox]:checked").each(function(idx){
				var checkbox = $(this);
				filters[checkbox.attr('name')] = checkbox.val();
			});
			$(this.filterEl + " select option:selected").each(function(idx){
				var option = $(this);
				if(option.val()){
					filters[option.parent().attr('name')] = option.val();
				}
			});
			return filters;
		},
		
	});
	
	return FilterView;
	
});


