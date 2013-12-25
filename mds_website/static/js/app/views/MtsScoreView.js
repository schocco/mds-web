/**
 * A nested view that displays the score object (either for UDH or UXC).
 */
define(['backbone',
        'cache',
        'text!templates/_UDH_score.html',
        'text!templates/_UXC_score.html',
        'jquery',
        'underscore'],
		function(Backbone, cache, udh_tpl, uxc_tpl, $, _){
	
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
			//this.score = options.score;
			this.el = $(options.parent);
			this.scale = options.scale;
			if(this.scale.score){
				console.log("no score yet!");
			}
			if(this.type.toLowerCase() == "udh"){
				this.tpl = udh_tpl;
				this.labeldict = $.extend({avg_slope: "Average slope (%)"}, this.labels);
			} else if(this.type.toLowerCase() == "uxc"){
				this.tpl = uxc_tpl;
				this.labeldict = $.extend({max_slope: "Maximum slope uphill (%)", total_ascent: "Total ascent (m)"}, this.labels)
			} else {
				throw new Error("type option must be 'udh' or 'uxc', but got " + type);
			}
			this.render();
			
		},
		
		render: function(){
			// render tpl with options object
			console.log("render MtsScoreView");
			if(!this.scale.score){
				this.scale.score = this.labeldict;
			}
			
			var compiledTemplate = _.template( this.tpl, {'scale': this.scale, 'labels': this.labeldict });
			$(this.el).html(compiledTemplate);
		}
		
			
	});
	
	return MtsScoreView;
	
});


