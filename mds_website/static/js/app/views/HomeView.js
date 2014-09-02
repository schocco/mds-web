define(['backbone',
        'cache',
        'underscore',
        'text!templates/home.html',
        'jquery',
        'views/BaseView',
        'jquery_localscroll',
        'jquery_scrollto'
        ],
		function(Backbone, cache, _, tpl, $, BaseView){
	
	var HomeView = BaseView.extend({
		el: '#content',
		title: "Home",
		
		initialize: function () {
			var that = this;
			this.trigger("initialize");
			BaseView.prototype.initialize.apply(this);
			
//		    _.bindAll(this, 'beforeRender', 'render', 'afterRender'); 
//		    var _this = this; 
//		    //can this code be put in a base class?
//		    this.render = _.wrap(this.render, function(render) { 
//		      that.beforeRender(); 
//		      render(); 
//		      that.afterRender(); 
//		      return _this; 
//		    }); 
			
			//TODO: change #header
		    this.render();
		    
		},
		render: function(){
			console.log("rendering home view");
			var compiledTemplate = _.template( tpl, {'meta': {} });
			this.setContent(compiledTemplate);
		},
		
		afterRender: function(){
			console.log("after render in homeview");
		}
		
			
	});
	
	return HomeView;
	
});


