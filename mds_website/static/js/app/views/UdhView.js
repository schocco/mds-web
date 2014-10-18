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
		
		showExample: function(){
			//TODO
			console.log("TODO: update calculator and scrollto top");
			
		}
		
			
	});
	
	return UdhView;
	
});


