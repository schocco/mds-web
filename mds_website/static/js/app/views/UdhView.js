/**
 * Calculator view for the UDH scale.
 */
define(['backbone',
        'underscore',
        'text!templates/udh.html',
        'jquery',
        'cache',
        'views/BaseView',
		'views/_ScoreWrapperView',
        'models/UDHModel',
        ],
		function(Backbone, _, tpl, $, cache, BaseView, ScoreWrapperView, UDH){
	
	var UdhView = BaseView.extend({
		el: '#content',
		title: "Unicycle Downhill Scale",
		
		initialize: function () {
			BaseView.prototype.initialize.apply(this);
			this.mscales = cache.get('MscaleCollection');
			this.scale = new UDH();
		    this.render();
		    
		},
		render: function(){
			var compiledTemplate = _.template( tpl, {'meta': {} });
			this.setContent(compiledTemplate);
			
			var options = {	
				parent: "#calculator",
				editable: true,
				type: "udh"
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
			var avgSlope = $("input[name=average_slope]");
			var avgDif = $("select[name=average_difficulty]");
			var maxDif = $("select[name=maximum_difficulty]");
			var length = $("input[name=total_length]");

			avgSlope.val(16);
			avgDif.val(1.5);
			maxDif.val(3.5);
			length.val(6000);
			
			this.scoreWrapperView.updateScore();
			
			//FIXME: scrolls to wrong position.
			$('html,body').animate({scrollTop: $("#calculator").offset().top},'slow');
	}
		
			
	});
	
	return UdhView;
	
});


