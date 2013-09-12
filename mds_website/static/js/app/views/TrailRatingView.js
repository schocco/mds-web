define(['backbone',
        'models/TrailModel',
        'underscore',
        'text!templates/trail_rating.html',
        'jquery',
        'openlayers',
        'jquery_form'],
		function(Backbone, Trail, _, tpl, $, OpenLayers){
	
	var TrailRatingView = Backbone.View.extend({
		el: '#content',		
		
		/**
		 * @param trail: trail obj or id
		 */
		initialize: function (trail) {
			var that = this;
			that.trail = trail; //Trail.get(trail);
			// create appropriate scale object
			if that.trail.get("type") == "downhill":
				that.scale = new UDH(); //TODO: define model
			else:
				that.scale = new UXC(); //TODO: define model
			that.render();
   
		    
		},
		
		/** renders the whole view. */
		render: function(){
			console.log("render template");
			//TODO: render template with appropriate form
		},
		
		/** add appropriate event handlers to the form */
		set_up_form: function(){
			var csrftoken = $('meta[name=csrf-token]').attr("content");
			var that = this;

			$('#rating_form').submit(function(){
				var data = $(this).serializeArray();
				//TODO: validate data
				return false;
			});
		},
		
		
		/** persist the rating object */
		save_rating: function(){
			//TODO: validate first
			// upload UXC or UDH object
		}
		
			
	});
	
	return TrailRatingView;
	
});


