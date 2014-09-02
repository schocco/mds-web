define(['backbone',
        'cache',
        'underscore',
        'text!templates/home.html',
        'jquery',
        'jquery_scrollto'
        ],
		function(Backbone, cache, _, tpl, $){
	
	var BaseView = Backbone.View.extend({
		el: '#content',
		title: "",
		
		initialize: function () {
			this.preInit();
			var that = this;
		    _.bindAll(this, 'beforeRender', 'render', 'afterRender'); 
		    this.render = _.wrap(this.render, function(render) { 
		      that.beforeRender(); 
		      render(); 
		      that.afterRender(); 
		      return that; 
		    }); 

		},
		
		
		beforeRender: function(){
			$("#header").css("min-height",50);
			$('#startButton').hide();
			var that = this;
			$('#logoCaption').fadeOut(function(){
				$(this).html(that.title).fadeIn(600);
			});
			$("html,body").animate({
			    scrollTop: 50,
			    scrollLeft: 0
			});
		},
		
		afterRender: function(){
			return;
		},
		
		preInit: function(){
			$(this.el).html('<section class="section"><div class="boxed"><div class="one-full"><p>loading...</p></div></div></section>');
		},
		
		setContent: function(content){
			$(this.el).fadeOut(function() {
				  $(this).html(content).fadeIn(600);
			});
		}
		
			
	});
	
	return BaseView;
	
});


