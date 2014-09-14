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
		
		settings: {	},

		/**
		 * Set the META returned by the API and return the resources.
		 */
		parse: function(response) {
			this.recentMeta = response.meta || {};
			return response.objects || response;
		},

		hasNextPage: function() {
			return this.recentMeta.next != null;
		},

		hasPreviousPage: function() {
			return this.recentMeta.previous != null;
		},
		
		getFirstPage: function() {
			this.fetch({reset: true, data: this.settings});
		},
		
		getLastPage: function() {
			var lastOffset = (this.getTotalPages - 1) * this.getOffset();
			var last = {offset: lastOffset};
			this.fetch({reset: true, data: _.extend(this.settings, last)});
		},

		getNextPage: function() {
			if(this.hasNextPage()){
				//transform query params to dict
				var nxt = this.recentMeta.next;
				nxt = nxt.substr(nxt.lastIndexOf("?")+1);
				var nxtDict = JSON.parse('{"' + nxt.replace(/&/g, '","').replace(/=/g,'":"') + '"}');
				this.fetch({reset: true, data: _.extend(nxtDict, this.settings)});
			}
		},

		getPreviousPage: function() {
			if(this.hasPreviousPage()){
				//transform query params to dict
				var prev = this.recentMeta.previous;
				prev = prev.substr(prev.lastIndexOf("?")+1);
				var prevDict = JSON.parse('{"' + prev.replace(/&/g, '","').replace(/=/g,'":"') + '"}');
				this.fetch({reset: true, data: _.extend(prevDict, this.settings)});
			}
		},

		getTotalPages: function() {
			return Math.ceil(this.recentMeta.total_count / this.recentMeta.limit);
		},

		getTotalItems: function() {
			return this.recentMeta.total_count;
		},
		
		setFilter: function(filter) {
			this.settings.filter = filter;
		},
		
		setSorting: function(sorting) {
			this.settings.sorting = sorting;
		},
		
		setOffset: function(offset) {
			this.settings.offset = offset;
		},
		
		getOffset: function() {
			return this.settings.offset || this.recentMeta.offset;
		}

	});

	return BaseCollection;

});




