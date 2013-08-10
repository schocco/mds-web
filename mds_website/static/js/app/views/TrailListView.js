define(['backbone',
        'collections/TrailCollection',
        'underscore',
        'text!templates/trail_list.html',
        'jquery',
        'chart'],
		function(Backbone, TrailsCollection, _, tpl, $){
	
	var TrailsView = Backbone.View.extend({
		el: '#content',
		initialize: function () {
			var that = this;
		    var onDataHandler = function(collection) {
		    	console.log("fetched data.");
		        that.render();
		    }
		    that.collection = new TrailsCollection([]);
		    that.collection.fetch({ success : onDataHandler });
		    this.collection.on("reset", this.render, this);
		},
		render: function(){
			console.log("rendering");
			console.log(this.collection.models);
			var compiledTemplate = _.template( tpl, {'trails': this.collection.models });
			$(this.el).html(compiledTemplate);
			
			var data = {
					labels : ["January","February","March","April","May","June","July"],
					datasets : [
						{
							fillColor : "rgba(220,220,220,0.5)",
							strokeColor : "rgba(220,220,220,1)",
							pointColor : "rgba(220,220,220,1)",
							pointStrokeColor : "#fff",
							data : [65,59,90,81,56,55,40]
						},
						{
							fillColor : "rgba(151,187,205,0.5)",
							strokeColor : "rgba(151,187,205,1)",
							pointColor : "rgba(151,187,205,1)",
							pointStrokeColor : "#fff",
							data : [28,48,40,19,96,27,100]
						}
					]
				}
			var ctx = document.getElementById("chart").getContext("2d");
			var myNewChart = new Chart(ctx).Line(data);
			
		},
			
	});
	
	return TrailsView;
	
});


