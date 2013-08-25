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
			//create map
			var WGS84 = new OpenLayers.Projection("EPSG:4326");
			var MERCATOR = new OpenLayers.Projection('EPSG:900913');
			var options = {
				    projection: WGS84 //WGS84
			};
			map = new OpenLayers.Map("mapdiv", options);
			var ol = new OpenLayers.Layer.OSM("osm");
			
			//create a linestring with all points given in the trails waypoints
			var coordinates = this.trail.get('waypoints').coordinates;
			var points = new Array();
			for (var i = 0; i < coordinates.length; i++) {
				points[i] = new OpenLayers.Geometry.Point(coordinates[i][0], coordinates[i][1]);
			}
			var linestring = new OpenLayers.Geometry.LineString(points).transform(WGS84, MERCATOR);

			// add track as vector layer to map
			var trail = new OpenLayers.Layer.Vector("Trail")
			trail.style = {strokeColor:"#0500bd", strokeWidth:3};
			
			trail.addFeatures([new OpenLayers.Feature.Vector(linestring)]);
			map.addLayers([ol,trail]);
			map.setCenter(new OpenLayers.LonLat(coordinates[0][0], coordinates[0][1]).transform(WGS84, MERCATOR), 14);	
			map.addControl(new OpenLayers.Control.LayerSwitcher());
			map.addControl(new OpenLayers.Control.MousePosition()); 
			
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


