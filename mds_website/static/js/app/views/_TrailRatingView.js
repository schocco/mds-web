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
        'jquery',
        'jquery_form'],
		function(Backbone, cache, Trail, UDH, UXC, ScoreView, MscaleCollection, _, tpl, $){
	
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
		},
		
		/** create appropriate scale object and listen for scale changes */
		read_trail_info: function(){
			if(this.trail.get("type") == "downhill"){
				this.type = "udh";
				// creates a new object or converts object to UDH model type
				this.scale = new UDH(this.trail.get("udh_rating"));
			}
			else if(this.trail.get("type") == "xc"){
				this.type = "uxc";
				// creates a new object or converts object to UDH model type
				this.scale = new UXC(this.trail.get("uxc_rating"));
			} else {
				console.log("Unknown type");
				this.scale = {};
			}
			// listen for changes of the scale object, and update score when it has changed
			// do not register in init method to ensure scale objects exists before listener registration
			this.listenTo(this.scale, "score_update", this.display_score);
		},
		
		/** renders the whole view. Adds either the udh or uxc form to the view. */
		render: function(){
			console.debug("render ratingview template");
			var compiledTemplate = _.template(tpl, {scale: this.scale, trail: this.trail});
			$(this.el).html(compiledTemplate);
			var options = {	parent: "#rating_div",
					type: this.type,
					scale: this.scale
				  }
			this.scoreView = new ScoreView(options);
			this.make_editable();
			this.set_up_form();	
		},
		
		/** replaces table cells with form fields to allow editing the rating. */
		make_editable: function(){
			//TODO: do not make editable when data is present or user is unauthorized to edit
			if(this.scale.get("id")){
				console.log("Do not make table editable, its already got a scale object");
				return;
			}
			//WARNING: naming is inconsistent. The scale has different names than the trail. This should be unified, alternatively
			// constants should be used.
			var values = { // use scale values and fallback to trail values
					max_difficulty: this.scale.get('maximum_difficulty'),
					length: this.scale.get('total_length') || this.trail.get('length').m,
					total_ascent: this.scale.get('total_ascent') || this.trail.get('total_ascent'),
					max_slope: this.scale.get('maximum_slope_uh') || this.trail.get('max_slope_uh'),
					avg_slope: this.scale.get('average_slope') || this.trail.get('avg_slope'),
					avg_difficulty: this.scale.get('average_difficulty')
					}
			var context = {trail: this.trail, mscales: this.mscales.models, scale: this.scale, values: values};
			var replacements = {
					max_difficulty: _.template('<select name="maximum_difficulty"><% _.each(mscales, function(mscale) { %> \
				          <option value="<%= mscale.get(\'id\') %>" <% if (values["max_difficulty"] ==  mscale.get(\'id\')) print("selected"); %>>m<%= mscale.get(\'id\') %></option><% }); %>\
				        </select>', context),
					total_length: _.template('<input type="number" name="total_length" value="<%= Math.round(values["length"]) %>"/>', context),
					total_ascent: _.template('<input type="number" name="total_ascent" value="<%= Math.round(values["total_ascent"]) %>"/>', context),
					max_slope: _.template('<input type="number" name="maximum_slope_uh" value="<%= Math.round(values["max_slope"]) %>"/>', context),
					avg_difficulty: _.template('<select name="average_difficulty"><% _.each(mscales, function(mscale) { %> \
					          <option value="<%= mscale.get(\'id\') %>" <% if (values["avg_difficulty"] ==  mscale.get(\'id\')) print("selected"); %>>m<%= mscale.get(\'id\') %></option><% }); %>\
					        </select>', context),
					avg_slope: _.template('<input type="number" name="average_slope" value="<%= Math.abs(Math.round(values["avg_slope"])) %>"/>', context),
			}; //contains udh and uxc fields
			
			for (var key in replacements) {
				$("#"+key).html(replacements[key]);
			}
		},
		
		/** add appropriate event handlers to the form.
		 * The form fields are re-rendered when an update of the data occurs, so that the
		 * input change listener needs to be bound again after a re-rendering. */
		set_up_form: function(){
			var csrftoken = $('meta[name=csrf-token]').attr("content");
			var that = this;
			//update scale object when form data is changed
			this.set_up_form_fields();
			//submit button
			$('#submit').click(function(evt){
				evt.preventDefault();
				$('#scale_form').submit();
			});
			//update button
			$('#update_score').click(function(evt){
				evt.preventDefault();
				that.update_score();
			});
			//form submission
			$('#scale_form').submit(function(evt){
				evt.preventDefault();
				that.save_score();
			});
		},
		
		/** update scale object when form data is changed */
		set_up_form_fields: function(){
			var that = this;
			//update scale object when form data is changed
			$('#scale_form').find(':input').change(function(src){
				that.form_change_handler(src, that.scale);
				that.update_score();
				});
		},
		
		/** 
		 * Triggers an ajax request to get the score of the scale object.
		 * The scale object triggers an event
		 * when it is done fetching the score.
		 **/
		update_score: function(){
			//make sure form values are stored in scale obj
			this.form_change_handler(null, this.scale);
			if(this.scale.isValid()){
				this.scale.get_score(); //triggers an update event
				this.reset_form_errors();
			} else{
				console.log("cannot get score, while obj isn't valid");
				console.log("Errors are:" + this.scale.validationError);
				this.show_form_errors(this.scale.validationError);
			}

		},
		
		/***
		 * Persists the current values of the scale in the backend.
		 * Makes the form non-editable.
		 */
		save_score: function(){
			//TODO: add error handling and success handler.
			//make sure the object is assigned to the current trail
			this.scale.set({"trail": this.trail.url()});
			this.scale.save();
		},
		
		show_form_errors: function(errors){
			var tpl = "<ul><% _.each(errors, function(err) { %><li><%= err %></li><% }); %></ul>";
			var rendered = _.template(tpl, {errors: errors});
			$("#form_errors").html(rendered);
			$("#form_errors").show({duration:300});
		},
		
		reset_form_errors: function(){
			$("#form_errors").html("");
			$("#form_errors").hide({duration: 0});
		},
		
		/** Callback function for the score_update event emitted by the scale object.
		 * Displays the values of the score object */
		display_score: function(error){
			if(error){
				console.error(error);
				//TODO display meaningful errors to user
			} else {
				var options = {	parent: "#rating_div",
								type: this.type,
								scale: this.scale
							  }
				this.scoreView.update(options);//this.scale);
				this.make_editable(); //TODO: should not be called after saving the object in the backend
				// need to bind change events after re-rendering:
				this.set_up_form_fields();
			}
		},
		
		
		/** handler that updates the values of the scale
		 * object when values are changed in the form. */
		form_change_handler: function(field, scale){
			var fields = $('#scale_form').serializeArray();
			var that = this;

			// the field names need to match the scale attribute names!
			$.each(fields, function(i, field){
				scale.set(field.name, field.value);
			});
			
		}
		
			
	});
	
	return _TrailRatingView;
	
});


