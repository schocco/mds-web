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
			var linestrings = new Array();


			// add track as vector layer to map
			var trail = new OpenLayers.Layer.Vector("Trail");
			var waypoints = new OpenLayers.Layer.Vector("Waypoints");
			trail.style = {strokeColor:"#0500bd", strokeWidth:3};
			// get all linestrings from multilinestring
			for (var k = 0; k < coordinates.length; k++) {
				ls = coordinates[k]
				console.log("create linestring #" + k);
				for (var i = 0; i < ls.length; i++) {
					points[i] = new OpenLayers.Geometry.Point(ls[i][0], ls[i][1]);
				}
				var linestring = new OpenLayers.Geometry.LineString(points).transform(WGS84, MERCATOR);
				linestrings[k] = linestring
			}
			var multi_ls = new OpenLayers.Geometry.MultiLineString(linestrings)//.transform(WGS84, MERCATOR);
			
			var lsFeature = new OpenLayers.Feature.Vector(multi_ls);
			trail.addFeatures(lsFeature);
			
			map.addLayers([ol,trail]);
			
			// set extend / zoom level
			var bounds = new OpenLayers.Bounds();
			var first_pt = coordinates[0][0];
			var last_pt = coordinates[coordinates.length-1][coordinates[coordinates.length-1].length-1]
			bounds.extend(new OpenLayers.LonLat(first_pt[0], first_pt[1]).transform(WGS84, MERCATOR));
			bounds.extend(new OpenLayers.LonLat(last_pt[0], last_pt[1]).transform(WGS84, MERCATOR));
			map.zoomToExtent(bounds);
			
			//add controls
			map.addControl(new OpenLayers.Control.LayerSwitcher());
			map.addControl(new OpenLayers.Control.MousePosition());
			
			if(this.editable){
				//TODO: allow moving and deleting points of the trail
				// see http://openlayers.org/dev/examples/modify-feature.html
				// new trail needs to be read from map and new elevation
				// data needs to be added in the backend or via a web service of OSM or gmaps
	            controls = {
	                   // line: new OpenLayers.Control.DrawFeature(trail,
	                   //             OpenLayers.Handler.Path),
	                    modify: new OpenLayers.Control.ModifyFeature(trail)
	            };
	            controls.modify.mode = OpenLayers.Control.ModifyFeature.RESHAPE;
	            controls.modify.createVertices = true;
	            for(var key in controls) {
	                map.addControl(controls[key]);
	                controls[key].selectFeature(lsFeature);
	                controls[key].activate();
	            }
			}
		}
			
	});
	
	return _MapView;
	
});

