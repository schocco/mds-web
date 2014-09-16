define(['backbone', 'models/TrailModel'],
		function(Backbone, Trail){


	var BaseCollection = Backbone.Collection.extend({
		/**
		 * Collection META that has been returned by the last query to the API.
		 */
		recentMeta: {
	        "limit": null,
	        "next": null,
	        "offset": null,
	        "previous": null,
	        "total_count": null
		},
		
		settings: {
			"offset": 0,
			"limit": 20
		},
		

		/**
		 * Set the META returned by the API and return the resources.
		 */
		parse: function(response) {
			this.recentMeta = response.meta || {};
			return response.objects || response;
		},
		
		url : function() {
			urlparams = {
					offset : this.settings.offset,
					limit : this.getPageSize()
			};
			urlparams = $.extend(urlparams, this.settings.filterOptions);
			if (this.settings.sortBy) {
				urlparams = $.extend(urlparams, {
					sort_by : this.settings.sortingOrder + this.settings.sortBy
				});
			}
			return this.baseUrl + '?' + $.param(urlparams);
		},

		hasNextPage: function() {
			return this.recentMeta.next != null;
		},

		hasPreviousPage: function() {
			return this.recentMeta.previous != null;
		},
		
		getPage: function(num){
			if(_.isNumber(num) && this.getTotalPages() >= num && num > 0){
				this.settings.offset = (num - 1) * this.getPageSize();
			}
			return this.fetch({reset: true});
		},
		
		getFirstPage: function() {
			this.getPage(1);
		},
		
		getLastPage: function() {
			getPage(this.getTotalPages());
		},

		getNextPage: function() {
			if(this.hasNextPage()){
				nxt = this.urlToDict(this.recentMeta.next);
				this.settings.offset = nxt.offset;
				this.fetch({reset: true});
			}
		},

		getPreviousPage: function() {
			if(this.hasPreviousPage()){
				prev = this.urlToDict(this.recentMeta.previous);
				this.settings.offset = prev.offset;
				this.fetch({reset: true});
			}
		},

		getTotalPages: function() {
			return Math.ceil(this.recentMeta.total_count / this.recentMeta.limit);
		},

		
		getTotalItems: function() {
			return this.recentMeta.total_count;
		},
		
		/**
		 * Provide filter options as a dictionary.
		 * {"name" : "abc"} becomes &name=abc
		 */
		setFilterOptions: function(filter) {
			// TODO: allow other comparators than =
			this.settings.filterOptions = filter;
			return this;
		},
		
		/**
		 * Sets the field that should be used for sorting.
		 */
		setSorting: function(sorting) {
			this.settings.sortBy = sorting;
			return this;
		},
		
		/**
		 * Sets the order for the sorting.
		 * Can be either "+" (ascendind) or "-" (descending)
		 */
		setSortOrder: function(order){
			if(order == "+" || order == "-" || order ==""){
				//+ is the default ordering, represented by empty str
				this.settings.sortingOrder = order.replace("+", "");
				return this;
			} else {
				throw "illegalArgument: must be '+' or '-'";
			}
			
		},
		
		
		setPageSize: function(size){
			if(_.isNumber(size) && size > 0){
				this.settings.limit = size;
				return this;
			} else {
				throw "illegalArgument: argument must be a positive integer";
			}
		},
		
		getPageSize: function(){
			return this.settings.limit || this.recentMeta.limit;
		},
		
		currentPageNumber: function(){
			return Math.floor(this.recentMeta.offset / this.getLimit) + 1;
		},
		
		/**
		 * Transforms query params to dict
		 */
		urlToDict: function(uri){
			queryParams = uri.substr(uri.lastIndexOf("?")+1);
			var dict = JSON.parse('{"' + queryParams.replace(/&/g, '","').replace(/=/g,'":"') + '"}');
			return dict;
		},
		
		clearSettings: function() {
			this.settings = {};
			return this;
		}
		


	});

	return BaseCollection;

});




