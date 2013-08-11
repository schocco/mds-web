define(['backbone',
        'models/TrailModel',
        'underscore',
        'text!templates/trail_detail.html',
        'jquery',
        'openlayers'],
		function(Backbone, Trail, _, tpl, $, OpenLayers){
	
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
		 * TODO: To be replaced. Data for the height profile should be provided by the server.
		 */
		get_chart_data: function(){
			var waypoints = this.trail.get('waypoints');
			var start = waypoints.coordinates[0][2] || 0;
			var end = waypoints.coordinates[waypoints.coordinates.length-1][2] || 0;
			
			var dataset = [];
			var labels = [];
			
			for(i=0;i<35;i++){
				  dataset[i] = Math.floor((Math.random()*10)+200);
				  labels[i] = i + " km";
			}
			
			var data = {
					labels : labels,//["Start height","End height"],
					datasets : [
						{
							fillColor : "rgba(151,187,205,0.5)",
							strokeColor : "rgba(151,187,205,1)",
							pointColor : "rgba(151,187,205,1)",
							pointStrokeColor : "#fff",
							data : dataset //[start,end]
						}
					]
				}
			return data;
		},
		
		
		/**
		 * Create and render an open layers map.
		 */
		render_map: function(){
			//create map
			map = new OpenLayers.Map("mapdiv");
			var ol = new OpenLayers.Layer.OSM();

			//create a linestring with all points given in the trails waypoints
			var coordinates = this.trail.get('waypoints').coordinates;
			var linestring = new OpenLayers.Geometry.LineString(coordinates);
			// add track as vector layer to map
			var vector = new OpenLayers.Layer.Vector();
			vector.addFeatures([new OpenLayers.Feature.Vector(linestring)]);
			map.addLayers([ol,vector]);
			map.setCenter(new OpenLayers.LonLat(1, 2), 3);	
		},
		
		
		render_height_profile: function(){
			var canvasdiv = document.getElementById("canvasdiv");
			var canvas = document.getElementById("height_profile");
			canvas.width = canvasdiv.clientWidth;
			canvas.height = canvasdiv.clientHeight;		
			var ctx = document.getElementById("height_profile").getContext("2d");
			var data = this.get_chart_data();
			// fixed scale
			var options = {
					scaleOverride : true,
					scaleSteps : 10,
					scaleStepWidth : 5,
					scaleStartValue : 190,
					pointDot : false,
					scaleLabel : "<%=value%> m"
				};
			console.log("render hight profile.");
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


