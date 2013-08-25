define(['backbone',
        'underscore',
        'jquery',
        'openlayers'],
		function(Backbone, _, $, OpenLayers){
	
	var _MapView = Backbone.View.extend({
		el: '#content',
		
		
		initialize: function (options) {
			console.log("init mapview");
			var that = this;
			this.el = options.parent;
			this.el_dom = $(this.el);
			this.geojson = options.geojson;
			this.height = options.height || 450;
			this.editable = options.editable || false;
			this.render_map();
		},
		
		
		/**
		 * Create and render an open layers map in the div passed in as parent.
		 * 
		 */
		render_map: function(){
			//clear container before inserting the map
			this.el_dom.empty();
			this.el_dom.height(this.height);
			//create map
			var WGS84 = new OpenLayers.Projection("EPSG:4326");
			var MERCATOR = new OpenLayers.Projection('EPSG:900913');
			var options = {
				    projection: WGS84 //WGS84
			};
			map = new OpenLayers.Map(this.el_dom.attr('id'), options);
			var ol = new OpenLayers.Layer.OSM("osm");
			
			//create a linestring with all points given in the trails waypoints
			var coordinates = this.geojson.coordinates;
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
			//map.setCenter(new OpenLayers.LonLat(coordinates[0][0], coordinates[0][1]).transform(WGS84, MERCATOR), 14);
			var bounds = new OpenLayers.Bounds();
			bounds.extend(new OpenLayers.LonLat(coordinates[0][0], coordinates[0][1]).transform(WGS84, MERCATOR));
			bounds.extend(new OpenLayers.LonLat(coordinates[coordinates.length-1][0], coordinates[coordinates.length-1][1]).transform(WGS84, MERCATOR));
			map.zoomToExtent(bounds);
			map.addControl(new OpenLayers.Control.LayerSwitcher());
			map.addControl(new OpenLayers.Control.MousePosition());	
			
			if(this.editable){
				//TODO: allow moving and deleting points of the trail
			}
		}
			
	});
	
	return _MapView;
	
});


