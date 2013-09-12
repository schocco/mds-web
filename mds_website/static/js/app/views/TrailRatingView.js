define(['backbone',
        'models/TrailModel',
        'models/UDHModel',
        'models/UXCModel',
        'underscore',
        'text!templates/trail_rating.html',
        'text!templates/_UDH_form.html',
        'text!templates/_UXC_form.html',
        'jquery',
        'jquery_form'],
		function(Backbone, Trail, UDH, UXC, _, tpl, udh_form, uxc_form, $){
	
	var TrailRatingView = Backbone.View.extend({
		el: '#content',		
		
		/**
		 * @param trail: trail obj or id
		 */
		initialize: function (options) {
			var that = this;
			that.trail = options.trail; //Trail.get(trail);
			that.scale = null;
			// create appropriate scale object
			if(that.trail.get("type") == "downhill"){
				that.scale = new UDH();
				that.form_tpl = udh_form;	
			}
			else{
				that.scale = new UXC();
				that.form_tpl = uxc_form;
			}

			that.render();
		},
		
		/** renders the whole view. Adds either the udh or uxc form to the view. */
		render: function(){
			console.debug("render ratingview template");
			var compiledTemplate = _.template(tpl, {scale: this.scale, trail: this.trail});
			$(this.el).html(compiledTemplate);
			//add form to div
			var compiledForm = _.template(this.form_tpl, {trail: this.trail});
			$('#form_container').html(compiledForm);
			this.set_up_form();
		},
		
		/** add appropriate event handlers to the form */
		set_up_form: function(){
			var csrftoken = $('meta[name=csrf-token]').attr("content");
			var that = this;

			$('#scale_form').submit(function(){
				var data = $(this).serializeArray();
				console.error("form processing not implemented yet");
				//TODO: validate data
				// set values for scale object
				return false;
			});
		},
		
		
		/** persist the rating object */
		save_rating: function(){
			//TODO: validate first
			// upload UXC or UDH object
		},
		
		/** handler that updates the preview of the result. */
		form_change_handler: function(){
			//TODO: submit scale object to get the scores, but don't save the object
		}
		
			
	});
	
	return TrailRatingView;
	
});


