define(['backbone',
        'cache',
        'underscore',
        'text!templates/home.html',
        'jquery',
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
				$(this).html(that.getTitle()).fadeIn(600);
			});
			document.title = (that.getTitle()) + " - Muni Difficulty Scale | A Tool to Measure Trail Difficulty";
			function getPos(el) {
			    for (var lx=0, ly=0;
			         el != null;
			         lx += el.offsetLeft, ly += el.offsetTop, el = el.offsetParent);
			    return {x: lx,y: ly};
			}
			
			$("html,body").animate({
			    scrollTop: 80,
			    scrollLeft: 0
			});
		},
		
		afterRender: function(){
			return;
		},
		
		preInit: function(){
			$(this.el).html('<section class="section"><div class="boxed"><div class="one-full"><p>loading...</p></div></div></section>');
		},
		
		setContent: function(content, call){
			this.$el.hide();
			this.$el.html(content).fadeIn(600, call);
		},
		
		/**
		 * @return the page title or an empty string if none is set
		 */
		getTitle: function(){
			if(this.title){
				return this.title;
			}
			console.warn("No title set.");
			return "";
		}
		
			
	});
	
	return BaseView;
	
});


