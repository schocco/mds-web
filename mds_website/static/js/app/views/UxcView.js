/**
 * Calculator view for the UDH scale.
 */
define(['backbone',
        'underscore',
        'text!templates/uxc.html',
        'jquery',
        'cache',
        'views/BaseView',
		'views/_ScoreWrapperView',
        'models/UXCModel',
        'mathjax'
        ],
		function(Backbone, _, tpl, $, cache, BaseView, ScoreWrapperView, UXC){
	
	var UxcView = BaseView.extend({
		el: '#content',
		title: "Unicycle Cross Country Scale",
		
		initialize: function () {
			BaseView.prototype.initialize.apply(this);
			this.mscales = cache.get('MscaleCollection');
			this.scale = new UXC();
		    this.render();
		    
		},
		render: function(){
			var compiledTemplate = _.template( tpl, {'meta': {} });
			this.setContent(compiledTemplate);
			
			var options = {	
				parent: "#calculator",
				editable: true,
				type: "uxc"
			 };
			this.scoreWrapperView = new ScoreWrapperView(options);
			this.scoreWrapperView.render();
			var that = this;
			
			$("#showInCalculator").click(function(e){
				e.preventDefault();
				that.showExample();
			});
		},
		
		/**
		 * Sets the values of the calculation example in the calculator table. 
		 */
		showExample: function(){
			//get form fields by name and set values
			var maxSlope = $("input[name=maximum_slope_uh]");
			var totalAsc = $("input[name=total_ascent]");
			var avgDif = $("select[name=average_difficulty]");
			var maxDif = $("select[name=maximum_difficulty]");
			var length = $("input[name=total_length]");

			length.val(42000);
			totalAsc.val(590);
			maxSlope.val(8);
			maxDif.val(1.5);
			avgDif.val(0.5);
						
			this.scoreWrapperView.updateScore();
			
			//FIXME: scrolls to wrong position.
			$('html,body').animate({scrollTop: $("#calculator").offset().top},'slow');
	}
		
			
	});
	
	return UxcView;
	
});


