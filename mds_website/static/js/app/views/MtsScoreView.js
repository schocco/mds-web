/**
 * A nested view that displays the score object (either for UDH or UXC).
 */
define(['backbone',
        'cache',
        'text!templates/_UDH_score.html',
        'text!templates/_UXC_score.html',
        'jquery'],
		function(Backbone, cache, udh_tpl, uxc_tpl, $){
	
	var MtsScoreView = Backbone.View.extend({
		el: null,
		type: null,
		tpl: null,
		score: null,
		
		/**
		 * @param type: type of the score object (either udh or uxc)
		 * @param score: the score object
		 * @param parent: parent dom element
		 */
		initialize: function(options) {
			this.type = options.type;
			this.score = options.score;
			this.el = $(options.parent);
			
			if(this.type.toLowerCase() == "udh"){
				this.tpl = udh_tpl;
			} else if(this.type.toLowerCase() == "uxc"){
				this.tpl = uxc_tpl;
			} else {
				throw new Error("type option must be 'udh' or 'uxc', but got " + type);
			}
			this.render();
			
		},
		
		render: function(){
			// render tpl with options object
			var compiledTemplate = _.template( this.tpl, {'score': this.score });
			$(this.el).html(compiledTemplate);
		}
		
			
	});
	
	return MtsScoreView;
	
});


