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
		
		/** get the current score of the scale object */
		update_score: function(){
			//make sure form values are stored in scale obj
			this.form_change_handler(null, this.scale);
			//get score obj
			if(this.scale.isValid()){
				score = this.scale.get_score();
				this.display_score(score);
			} else{
				console.log("cannot get score, while obj isn't valid");
				console.log("Errors are:" + this.scale.validationError);
			}

		},
		
		/** display the values of the score object */
		display_score: function(score){
			console.error("not yet implemented");
			console.log(score);
		},
		
		/** persist the rating object */
		save_rating: function(){
			//TODO: make sure scale is complete and linked to the current trail.
			this.scale.save();
		},
		
		/** handler that updates the preview of the result. */
		form_change_handler: function(field, scale){
			var fields = $('#scale_form').serializeArray();
			var that = this;
			$.each(fields, function(i, field){
				console.log(field);
				scale.set(field.name, field.value);
			});
			
		}
		
			
	});
	
	return TrailRatingView;
	
});


