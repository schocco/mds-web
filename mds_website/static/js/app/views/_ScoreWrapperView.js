/**
 * A wrapper view around the MtsScoreView which adds additional functionality.
 * Lays out the score table and the chart side by side.
 * The data table can be turned into a form.
 */

define(['backbone',
        'cache',
        'models/TrailModel',
        'models/UDHModel',
        'models/UXCModel',
        'views/MtsScoreView',
        'collections/MscaleCollection',
        'underscore',
        'text!templates/_score_wrapper.html',
        'jquery',
        //'jquery_form'
        ],
		function(Backbone, cache, Trail, UDH, UXC, ScoreView, MscaleCollection, _, tpl, $){
	
	var _ScoreWrapperView = Backbone.View.extend({
		
		/**
		 * @param parent: container in which view should be rendered
		 * @param type: either "UDH" or "UXC"
		 * @param editable (boolean)
		 */
		initialize: function (options) {
			this.scale = null;
			this.trail = options.trail; //optional
			this.editable = options.editable;
			this.el = options.parent;
			this.ratingDiv = "#ratingDiv"; //div for the scoreView
			this.mscales = cache.get('MscaleCollection');
			this.type = options.type;
			
			this.createScaleObj();
			this.saveable = this.trail != null && this.editable;
		},
		
		/** create appropriate scale object and listen for scale changes */
		createScaleObj: function(){
			if(this.trail != null){
				if(this.trail.get("type") == "downhill"){
					this.type = "udh";
					// creates a new object or converts object to UDH model type
					this.scale = new UDH(this.trail.get("udh_rating"));
				}
				else if(this.trail.get("type") == "xc"){
					this.type = "uxc";
					// creates a new object or converts object to UXC model type
					this.scale = new UXC(this.trail.get("uxc_rating"));
				} 
			} else if(this.type != null){
				if(this.type == "udh"){
					this.scale = new UDH();
				}
				else if(this.type == "uxc"){
					this.scale = new UXC();
				}
			} else {
				throw "Unknown scale type!";
			}
			// listen for changes of the scale object, and update score when it has changed
			// do not register in init method to ensure scale objects exist before listener registration
			this.listenTo(this.scale, "score_update", this.displayScore);
			if(this.scale.get("id")){
				//scale already persisted, so not editable
				this.editable = false;
			}
		},

		
		/** renders the whole view. Adds either the udh or uxc form to the view. */
		render: function(){
			var compiledTemplate = _.template(tpl)({
				scale: this.scale, 
				editable: this.editable,
				saveable: this.saveable
				});
			$(this.el).html(compiledTemplate);
			var options = {	
					parent: this.ratingDiv,
					type: this.type,
					scale: this.scale,
					tableDiv: "ratingDiv",
					chartDiv: "radarChartDiv",
					canvasId: "chartCanvas"
			};
			this.scoreView = new ScoreView(options);
			if(this.editable){
				this.makeEditable();
			}
			
			var that = this;
			// bind save button and form submission (only required once, form is not re-rendered.)
			$('#submit').click(function(evt){
				evt.preventDefault();
				$('#scale_form').submit();
			});
			//form submission
			$('#scale_form').submit(function(evt){
				evt.preventDefault();
				that.saveScore();
			});
		},
		
		
		getValues: function(){
			//FIXME: naming is inconsistent. The scale has different names than the trail. This should be unified, alternatively
			// constants should be used.
			var values = { // use scale values and fallback to trail values
					max_difficulty: this.scale.get('maximum_difficulty'),
					length: this.scale.get('total_length') || this.trail && this.trail.get('length').m,
					total_ascent: this.scale.get('total_ascent') || this.trail && this.trail.get('total_ascent'),
					max_slope: this.scale.get('maximum_slope_uh') || this.trail && this.trail.get('max_slope_uh'),
					avg_slope: this.scale.get('average_slope') || this.trail && this.trail.get('avg_slope'),
					avg_difficulty: this.scale.get('average_difficulty')
				};
			return values;
		},

		
		
		/** replaces table cells with form fields to allow editing the rating. */
		makeEditable: function(){
			if(this.scale.get("id")){
				console.log("Do not make table editable, its already got a scale object");
				return;
			}
			var values = this.getValues();
			var context = {trail: this.trail, mscales: this.mscales.models, scale: this.scale, values: values};
			var replacements = {
					max_difficulty: _.template('<select name="maximum_difficulty"><% _.each(mscales, function(mscale) { %> \
				          <option value="<%= mscale.get(\'id\') %>" <% if (values["max_difficulty"] ==  mscale.get(\'id\')) print("selected"); %>>M<%= mscale.get(\'id\') %></option><% }); %>\
				        </select>')(context),
					total_length: _.template('<input type="number" name="total_length" value="<%= Math.round(values["length"]) %>"/>')(context),
					total_ascent: _.template('<input type="number" name="total_ascent" value="<%= Math.round(values["total_ascent"]) %>"/>')(context),
					max_slope: _.template('<input type="number" name="maximum_slope_uh" value="<%= Math.round(values["max_slope"]) %>"/>')(context),
					avg_difficulty: _.template('<select name="average_difficulty"><% _.each(mscales, function(mscale) { %> \
					          <option value="<%= mscale.get(\'id\') %>" <% if (values["avg_difficulty"] ==  mscale.get(\'id\')) print("selected"); %>>M<%= mscale.get(\'id\') %></option><% }); %>\
					        </select>')(context),
					avg_slope: _.template('<input type="number" name="average_slope" value="<%= Math.abs(Math.round(values["avg_slope"])) %>"/>')(context),
			}; //contains udh and uxc fields
			
			for (var key in replacements) {
				$("#"+key).html(replacements[key]);
			}
			this.setUpForm();
		},
		
		/** Add appropriate event handlers to the form.
		 * The form fields are re-rendered when an update of the data occurs, so that the
		 * input change listener needs to be bound again after a re-rendering. */
		setUpForm: function(){
			var csrftoken = $('meta[name=csrf-token]').attr("content");
			var that = this;
			//update scale object when form data is changed
			this.setUpFormFields();
		},
		
		/** update scale object when form data is changed */
		setUpFormFields: function(){
			var that = this;
			//update scale object when form data is changed
			$('#scale_form').find(':input').change(function(src){
				that.formChangeHandler(src, that.scale);
				that.updateScore();
				});
		},
		
		/** 
		 * Triggers an ajax request to get the score of the scale object.
		 * The scale object triggers an event
		 * when it is done fetching the score.
		 **/
		updateScore: function(){
			//make sure form values are stored in scale obj
			this.formChangeHandler(null, this.scale);
			if(this.scale.isValid()){
				this.scale.get_score(); //triggers an update event
				this.hideMessage();
			} else{
				this.showMessage({type:this.ERROR, msg:this.scale.validationError});
			}

		},
		
		/***
		 * Persists the current values of the scale in the backend.
		 * Makes the form non-editable.
		 */
		saveScore: function(){
			//make sure the object is assigned to the current trail
			var that = this;
			this.scale.set({"trail": this.trail.url()});
			this.scale.save(null, {
			    success: function (model, response) {
			        // update the score view, no longer editable
			    	that.scale = model;
			    	that.showMessage({type:that.INFO, msg:"The score has been saved."});
			    	that.displayScore();
			    	$("#submit").hide();
			    },
			    error: function (model, response) {
			        that.showMessage({type:that.ERROR, msg:response.responseText});
			    }});
		},
		
		/** Callback function for the score_update event emitted by the scale object.
		 * Displays the values of the score object */
		displayScore: function(error){
			if(error){
				console.error(error);
				//TODO display meaningful errors to user
			} else {
				var options = {	parent: this.ratingDiv,
								type: this.type,
								scale: this.scale
							 };
				this.scoreView.update(options);
				if(this.editable){
					this.makeEditable();
					// need to bind change events after re-rendering:
					this.setUpFormFields();
				}

			}
		},
		
		
		/** handler that updates the values of the scale
		 * object when values are changed in the form. */
		formChangeHandler: function(field, scale){
			var fields = $('#scale_form').serializeArray();
			var that = this;

			// the field names need to match the scale attribute names!
			$.each(fields, function(i, field){
				scale.set(field.name, field.value);
			});
		},
		
		/**
		* Makes the table editable. Editable status will remain after re-rendering.
		*/
		setEditable: function(flag){
			this.editable = flag;
		},
		
		setScale: function(scale){
			this.scale = scale;
		},
		
		setTrail: function(trail){
			this.trail = trail;
		}
		
			
	});
	
	return _ScoreWrapperView;
	
});


