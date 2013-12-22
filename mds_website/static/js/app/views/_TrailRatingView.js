/**
 * A wrapper view around the MtsScoreView which adds additional functionality for updating values.
 * Turns the data table into a form.
 */

define(['backbone',
        'cache',
        'models/TrailModel',
        'models/UDHModel',
        'models/UXCModel',
        'views/MtsScoreView',
        'collections/MscaleCollection',
        'underscore',
        'text!templates/_trail_rating.html',
        'text!templates/_UDH_form.html',
        'text!templates/_UXC_form.html',
        'jquery',
        'jquery_form'],
		function(Backbone, cache, Trail, UDH, UXC, ScoreView, MscaleCollection, _, tpl, udh_form, uxc_form, $){
	
	var _TrailRatingView = Backbone.View.extend({
		el: '#content',		
		
		/**
		 * @param trail: trail obj
		 * @param id: trail id must be given if no trail object is provided
		 * @param parent: container in which view should be rendered
		 */
		initialize: function (options) {
			var that = this;
			this.scale = null;
			this.ctr = 0;
			this.el = options.parent;
			
			//load mscales synchronously to avoid callback magic that would be required to sync with loading of trail object
			that.mscales = cache.get('MscaleCollection', MscaleCollection, {async:false});
			console.log(this.mscales);
			
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
				this.type = "udh";
				this.scale = new UDH();
				this.form_tpl = udh_form;	
			}
			else{
				this.type = "uxc";
				this.scale = new UXC();
				this.form_tpl = uxc_form;
			}
		},
		
		/** renders the whole view. Adds either the udh or uxc form to the view. */
		render: function(){
			console.debug("render ratingview template");
			var compiledTemplate = _.template(tpl, {scale: this.scale, trail: this.trail});
			$(this.el).html(compiledTemplate);
			//TODO: add score view to div
			//TODO: make table editable
			
//			var compiledForm = _.template(this.form_tpl, {trail: this.trail, mscales: this.mscales.models});
//			$('#form_container').html(compiledForm);
//			this.set_up_form();
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
		 * The scale object triggers an event
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
		
		/** Callback function for the score_update event emitted by the scale object.
		 * Displays the values of the score object */
		display_score: function(error){
			if(error){
				console.error(error);
			} else {
				var options = {	parent: "#rating_div",
								type: this.type,
								score: this.scale.score
							  }
				//TODO: use update method instead of recreating view
				this.scoreView = new ScoreView(options);
			}
		},
		
		
		/** handler that updates the values of the scale
		 * object when values are changed in the form. */
		form_change_handler: function(field, scale){
			var fields = $('#scale_form').serializeArray();
			var that = this;
			$.each(fields, function(i, field){
				scale.set(field.name, field.value);
			});
			
		}
		
			
	});
	
	return _TrailRatingView;
	
});


