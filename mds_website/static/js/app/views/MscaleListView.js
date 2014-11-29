define(['backbone',
        'cache',
        'underscore',
        'views/BaseView',
        'views/generic/FilteredListView',
        'text!templates/mscales.html',
        'text!templates/mscale_item.html',
        'jquery',
        ],
		function(Backbone, cache, _, BaseView, FilteredListView, tpl, itemTpl, $){
	
	var MscalesView = BaseView.extend({
		
		title: "M-Scale",
		
		initialize: function () {
			BaseView.prototype.initialize.apply(this);
			var that = this;
			this.mscales = cache.get('MscaleCollection');   
			this.render();
		},
		
		render: function(){
			var compiled = _.template(tpl)({mscales: this.mscales});
			this.setContent(compiled);
			//add items
			var items = $("#items");
			var itemTemplate = _.template(itemTpl);
			this.mscales.each(function(item){
				if(!item.isPseudo()){
					var itemDiv = itemTemplate({item: item});
					items.append(itemDiv);
					console.log(item);
				}
			});
			this.drawSlopes();
		},
		
		/**
		 * Draw a line that represents the slope into all canvases on the page
		 */
		drawSlopes: function(){
			var canvases = $("canvas");
			canvases.each(function(idx){
				var itm = $(this);
				var itmClass = itm.attr("class");
				var itmSize = Number(itm.width());
				if(itmClass.match(/slope-\d+/g)){
					var ctx = this.getContext('2d');
					var slope = Number(itmClass.replace(/\D/g, ''));
					console.log("Drawing slope " + slope);
					
					// the slope
					ctx.beginPath();
				    ctx.moveTo(0, itmSize-itmSize*slope/100);
				    ctx.lineTo(itmSize, itmSize);
				    ctx.stroke();
				    
				    // left, top to bottom
				    ctx.beginPath();
				    ctx.moveTo(0, itmSize-itmSize*slope/100);
				    ctx.lineTo(0, itmSize);
				    ctx.stroke();
				    
				    // bottom left to bottom right
				    ctx.beginPath();
				    ctx.moveTo(0, itmSize);
				    ctx.lineTo(itmSize, itmSize);
				    ctx.stroke();
				}
			});
			
		}
			
	});
	
	return MscalesView;
	
});


