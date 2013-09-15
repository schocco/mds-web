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
		 * @param trail: trail obj
		 * @param id: trail id must be given if no trail object is provided
		 */
		initialize: function (options) {
			var that = this;
			that.scale = null;
		    var onDataHandler = function(model) {
		    	that.read_trail_info();
		        that.render();
		    }
			if(options.trail == undefined){
				that.trail = new Trail({id: that.id});
			    that.trail.fetch({success: onDataHandler});
			} else{
				that.trail = options.trail;
				that.read_trail_info();
				that.render()
			}
			
			//listen for changes of the scale object, and update score when it has changed
			this.listenTo(this.scale, "score_update", this.display_score);
		},
		
		/** create appropriate scale object */
		read_trail_info: function(){
			if(this.trail.get("type") == "downhill"){
				this.scale = new UDH();
				this.form_tpl = udh_form;	
			}
			else{
				this.scale = new UXC();
				this.form_tpl = uxc_form;
			}
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
			//update scale object when form data is changed
			$('#scale_form').find(':input').change(function(src){
				that.form_change_handler(src, that.scale);
				that.update_score();
				});
			
			$('#submit').click(function(evt){
				evt.preventDefault();
				$('#scale_form').submit();
			});
			
			$('#update_score').click(function(evt){
				evt.preventDefault();
				that.update_score();
			});
			
			$('#scale_form').submit(function(evt){
				evt.preventDefault();
				that.save_rating();
			});
		},
		
		/** 
		 * Trigger an ajax request to get the score of the scale object.
		 * if the scale object is valid. The scale object triggers an event
		 * when it is done fetching the score.
		 **/
		update_score: function(){
			//make sure form values are stored in scale obj
			this.form_change_handler(null, this.scale);
			if(this.scale.isValid()){
				this.scale.get_score();
			} else{
				console.log("cannot get score, while obj isn't valid");
				console.log("Errors are:" + this.scale.validationError);
			}

		},
		
		/** Callbank function for the score_update event emitted by the scale object
		 * Displays the values of the score object */
		display_score: function(error){
			if(error){
				console.log(error);
			} else{
				console.log(this.scale.score);
			}
			console.error("not yet implemented");
			
		},
		
		
		/** handler that updates the values of the scale
		 * object when values are change din the form. */
		form_change_handler: function(field, scale){
			var fields = $('#scale_form').serializeArray();
			var that = this;
			$.each(fields, function(i, field){
				scale.set(field.name, field.value);
			});
			
		}
		
			
	});
	
	return TrailRatingView;
	
});


