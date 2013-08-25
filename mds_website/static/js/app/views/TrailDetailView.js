define(['backbone',
        'models/TrailModel',
        'views/_MapView',
        'underscore',
        'text!templates/trail_detail.html',
        'jquery',
        'openlayers'],
		function(Backbone, Trail, MapView, _, tpl, $, OpenLayers){
	
	var TrailDetailView = Backbone.View.extend({
		el: '#content',
		
		
		initialize: function (options) {
			var that = this;
		    var onDataHandler = function(model) {
		    	console.log("fetched trail");
		        that.render();
		    }
		    that.id = options.id;
		    that.trail = new Trail({id: that.id});
		    that.trail.fetch({success: onDataHandler});
		},
		
		/**
		 * Use the models waypoints to provide a dataset for chart.js
		 */
		get_chart_data: function(profile){
			var dataset = [];
			var labels = [];
		
			var data = {
					labels : profile.labels,
					datasets : [
						{
							fillColor : "rgba(151,187,205,0.5)",
							strokeColor : "rgba(151,187,205,1)",
							pointColor : "rgba(151,187,205,1)",
							pointStrokeColor : "#fff",
							data : profile.values
						}
					]
				}
			return data;
		},
		
		
		/**
		 * Create and render an open layers map.
		 */
		render_map: function(){
			this.mapview = new MapView({parent: "#mapdiv", geojson:this.trail.get("waypoints")});
		},
		
		
		render_height_profile: function(){
			var canvasdiv = document.getElementById("canvasdiv");
			var canvas = document.getElementById("height_profile");
			canvas.width = canvasdiv.clientWidth;
			canvas.height = canvasdiv.clientHeight;		
			var ctx = document.getElementById("height_profile").getContext("2d");
			
			
			var profile = this.trail.get('height_profile');
			var data = this.get_chart_data(profile);
			
			// fixed scale
			var options = {
					scaleOverride : true,
					scaleSteps : 10,
					scaleStepWidth : (profile.max_height - profile.min_height + 10) / 10,
					scaleStartValue : profile.min_height - 5,
					pointDot : false,
					scaleLabel : "<%=value%> m"
				};
			var myNewChart = new Chart(ctx).Line(data, options);
		},
		
		/** renders the whole view. */
		render: function(){
			console.log("render template");
			var compiledTemplate = _.template( tpl, {'trail': this.trail });
			$(this.el).html(compiledTemplate);
			
			console.log("create hight profile");
			this.render_height_profile();
			
			console.log("create map.");
			this.render_map();
			
		}
			
	});
	
	return TrailDetailView;
	
});


