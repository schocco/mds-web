/**
 * A nested view that displays the score object (either for UDH or UXC).
 */
define(['backbone',
        'cache',
        'text!templates/_MTS_score.html',
        'jquery',
        'underscore'],
		function(Backbone, cache, tpl, $, _){
	
	var MtsScoreView = Backbone.View.extend({
		el: null,
		type: null,
		tpl: null,
		score: null,
		labeldict: null, //dictionary to use for the template rendering
		labels: {avg_difficulty: "Average difficulty (M-Scale)",
				max_difficulty: "Maximum difficulty (M-Scale)",
				total_length: "Total length (m)",
				total_score: "Total score"
				},
		
		/**
		 * @param type: type of the score object (either udh or uxc)
		 * @param scale: the scale object (UDH or UXC)
		 * @param parent: parent dom element
		 * @param editable: true when data should be editable (default: false)
		 */
		initialize: function(options) {
			this.type = options.type;
			this.el = options.parent;
			this.tableDiv = options.tableDiv;
			this.chartDiv = options.chartDiv;
			this.canvasId = options.canvasId;
			this.scale = options.scale;
			this.tpl = tpl;

			if(this.type.toLowerCase() == "udh"){
				this.labeldict = $.extend({avg_slope: "Average slope (%)"}, this.labels);
			} else if(this.type.toLowerCase() == "uxc"){
				this.labeldict = $.extend({max_slope: "Maximum slope uphill (%)", total_ascent: "Total ascent (m)"}, this.labels);
			} else {
				throw new Error("type option must be 'udh' or 'uxc', but got " + type);
			}
			this.render();
			
		},
		
		render: function(){
			// render tpl with options object
			console.log("render MtsScoreView");
			if(!this.scale.get("score")){
				this.scale.set("score", this.labeldict);
			}
			
			var compiledTemplate = _.template( this.tpl)(
				{'scale': this.scale, 'labels': this.labeldict });
			$(this.el).html(compiledTemplate);
			this.draw_score_chart();
		},
		
		/**
		 * refresh the view, using information of a new scale object
		 */
		update: function(options){
			console.log("update MtsScoreView with this scale object: ");
			console.log(options.scale);
			this.scale = options.scale;
			if(!this.scale.get("score")){
				throw "Update Error: Need a scale object with score data";
			}
			var compiledTemplate = _.template( this.tpl)({'scale': this.scale, 'labels': this.labeldict });
			$(this.el).html(compiledTemplate);
			this.draw_score_chart();
		},	
		
		/**
		 * Draw a radar chart representation of the score.
		 */
		draw_score_chart: function(){
			var options = {//scaleShowLabels : true,
					//datasetStroke : false,
					scaleLineColor : "rgba(0,0,0,.15)",
					scaleOverride : true,
					scaleStepWidth : 1,
					scaleSteps : 10
					};
			var score = this.scale.get("score");
			
			//set size
			console.log("chartdiv is " + this.chartDiv);
		    var div = document.getElementById(this.chartDiv);
			var canvas = document.getElementById(this.canvasId);
			console.log("canvasDiv size:");
			console.log("h:" + div.offsetHeight + " w:" + div.offsetWidth);
			canvas.height = div.offsetWidth - 10;
			canvas.width  = div.offsetWidth;
			
			if(this.type == "udh"){
				// UDH
				var scoreData = [score['avg_slope'].result,
				                 score['avg_difficulty'].result,
				                 score['max_difficulty'].result,
				                 score['total_length'].result];
				var data = {
						labels : ["Avg Slope","Avg Difficulty","Max Difficulty","Length"],
						datasets : [
							{
								fillColor : "rgba(151,187,205,0.2)",
								strokeColor : "rgba(151,187,205,1)",
								pointColor : "rgba(151,187,205,1)",
								pointStrokeColor : "#fff",
								data : scoreData
							}
						]
				};
				var ctx = document.getElementById(this.canvasId).getContext("2d");
				new Chart(ctx).Radar(data,options);
			} else {
				// UXC 
				var scoreData = [score['avg_difficulty'].result/score['avg_difficulty'].max*10,
				                 score['max_difficulty'].result/score['max_difficulty'].max*10,
				                 score['max_slope'].result/ score['max_slope'].max*10,
				                 score['total_ascent'].result/score['total_ascent'].max*10,
								 score['total_length'].result/score['total_length'].max*10];
				var data = {
						labels : ["Avg difficulty","Max difficulty","Max slope","Total ascent", "Total length"],
						datasets : [
							{
								fillColor : "rgba(151,187,205,0.2)",
								strokeColor : "rgba(151,187,205,1)",
								pointColor : "rgba(151,187,205,1)",
								pointStrokeColor : "#fff",
								data : scoreData
							}
						]
				};
				var ctx = document.getElementById(this.canvasId).getContext("2d");
				new Chart(ctx).Radar(data,options);
			}
			
		}
		
		
			
	});
	
	return MtsScoreView;
	
});


