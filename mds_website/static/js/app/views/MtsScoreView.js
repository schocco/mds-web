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
		labels: {avg_difficulty: "Average difficulty (MTS)",
				max_difficulty: "Maximum difficulty (MTS)",
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
			console.log(options);
			this.type = options.type;
			this.el = $(options.parent);
			this.scale = options.scale;
			this.tpl = tpl;
			if(this.scale.get("score")){
				console.log("no score yet!");
			}
			if(this.type.toLowerCase() == "udh"){
				this.labeldict = $.extend({avg_slope: "Average slope (%)"}, this.labels);
			} else if(this.type.toLowerCase() == "uxc"){
				this.labeldict = $.extend({max_slope: "Maximum slope uphill (%)", total_ascent: "Total ascent (m)"}, this.labels)
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
			
			var compiledTemplate = _.template( this.tpl, {'scale': this.scale, 'labels': this.labeldict });
			$(this.el).html(compiledTemplate);
			this.draw_score_chart();
		},
		
		/**
		 * refresh the view, using information of a new scale object
		 */
		update: function(scale){
			console.log("update MtsScoreView");
			if(!this.scale.get("score")){
				throw "Update Error: Need a scale object with score data";
			}
			var compiledTemplate = _.template( this.tpl, {'scale': this.scale, 'labels': this.labeldict });
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
					//scaleOverride : true,
					//scaleStepWidth : 1,
					//scaleSteps : 10
					};
			var data = {
					labels : ["Max Slope UH","Total Ascent","Avg. MDS","Max. MDS","Length"],
					datasets : [
						{
							fillColor : "rgba(220,120,220,0.2)",
							strokeColor : "rgba(220,220,220,1)",
							pointColor : "rgba(220,220,220,1)",
							pointStrokeColor : "#fff",
							data : [20,20,38,40,35]
						},
						{
							fillColor : "rgba(151,187,205,0.2)",
							strokeColor : "rgba(151,187,205,1)",
							pointColor : "rgba(151,187,205,1)",
							pointStrokeColor : "#fff",
							data : [15,70,50,50,18]
						}
					]
				}
			var ctx = document.getElementById("score_chart").getContext("2d");
			new Chart(ctx).Radar(data,options);
			
		}
		
		
			
	});
	
	return MtsScoreView;
	
});


