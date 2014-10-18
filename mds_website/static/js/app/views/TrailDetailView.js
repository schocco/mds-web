define(['backbone',
        'models/TrailModel',
        'views/_MapView',
        'views/_ScoreWrapperView',
        'views/BaseView',
        'underscore',
        'text!templates/trail_detail.html',
        'jquery',
        'openlayers',
        'chart'],
		function(Backbone, Trail, MapView, ScoreWrapperView, BaseView, _, tpl, $, OpenLayers, chart){
	
	var TrailDetailView = BaseView.extend({
		el: '#content',
		
		
		initialize: function (options) {
			var that = this;
			BaseView.prototype.initialize.apply(this);
		    var onDataHandler = function(model) {
		    	console.log("fetched trail");
		        that.render();
		    };
		    if(options.id){
		    	//XXX: cannot use trail from cached collection as some fields are only available in the detail view
			    that.id = options.id;
			    that.trail = new Trail({id: that.id});
			    that.trail.fetch({success: onDataHandler});	
		    } else if(options.trail){
		    	that.trail = new Trail(options.trail);
		    	that.render();
		    } else{
		    	throw "missing argument, need either id or trail";
		    }
		},

		getTitle: function(){
			console.log(this);
			return "Trail details of '" + this.trail.get('name') + "'";
			
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
			};
			return data;
		},
		
		
		/**
		 * Create and render an open layers map.
		 */
		render_map: function(){
			this.mapview = new MapView({parent: "#mapdiv", geojson: this.trail.get("waypoints")});
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
					scaleStepWidth : Math.round((profile.max_height - profile.min_height + 10)) / 10,
					scaleStartValue : Math.round(10* profile.min_height - 5)/10,
					pointDot : false,
					scaleLabel : "<%=value%> m",
					scaleLineColor : "rgba(0,0,0,.3)",
					scaleGridLineColor : "rgba(0,0,0,.15)",
					bezierCurve : false,
				};
			var heightProfileChart = new Chart(ctx).Line(data, options);
		},
		
		render_score: function(){
			this.scoreview = new ScoreWrapperView({
				parent: "#score_div",
				trail: this.trail,
				editable: true
			});
			this.scoreview.render();
		},
		
		/** renders the whole view. */
		render: function(){
			var compiledTemplate = _.template( tpl, {'trail': this.trail });
			this.setContent(compiledTemplate);
			console.log("create hight profile");
			this.render_height_profile();
			
			console.log("create map.");
			this.render_map();
			
			console.log("create score/rating view");
			this.render_score();
		}
			
	});
	
	return TrailDetailView;
	
});


