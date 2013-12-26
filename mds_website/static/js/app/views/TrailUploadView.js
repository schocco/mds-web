define(['backbone',
        'models/TrailModel',
        'views/_MapView',
        'views/_TrailRatingView',
        'underscore',
        'text!templates/trail_upload.html',
        'jquery',
        'openlayers',
        'jquery_form'],
		function(Backbone, Trail, MapView, RatingView, _, tpl, $, OpenLayers){
	
	var TrailUploadView = Backbone.View.extend({
		el: '#content',		
		
		initialize: function () {
			var that = this;
			that.trail = new Trail();
			that.render();
   
		    
		},
		
		/** renders the whole view. */
		render: function(){
			console.log("render template");
			var compiledTemplate = _.template(tpl, {type_choices: this.trail.type_choices});
			$(this.el).html(compiledTemplate);		
			this.set_up_form()
		},
		
		/** add appropriate event handlers to the form */
		set_up_form: function(){
			
			var bar = $('.bar');
			var percent = $('.percent');
			var status = $('#status');
			var csrftoken = $('meta[name=csrf-token]').attr("content");
			var that = this;
			$('#upload_form').ajaxForm({
			    beforeSend: function(xhr, settings) {
			        status.empty();
			        var percentVal = '0%';
			        bar.width(percentVal)
			        percent.html(percentVal);
			        xhr.setRequestHeader("X-CSRFToken", csrftoken);
			    },
			    url: "load-gpx/",
			    dataType: "json",
			    uploadProgress: function(event, position, total, percentComplete) {
			        var percentVal = percentComplete + '%';
			        bar.width(percentVal)
			        percent.html(percentVal);
			    },
			    success: function() {
			        var percentVal = '100%';
			        bar.width(percentVal)
			        percent.html(percentVal);
			    },
				complete: function(xhr) {
					that.trail.set({waypoints: JSON.parse(xhr.responseText)});
					// toggle visibility
					$('#import_div').addClass("hidden");
					$('#info_div').removeClass('hidden');
					that.show_map();
				}
			}); 

			//trigger submit when upload link is clicked
			$('#submit').click(function() {
				$('#upload_form').submit();
				return false;
			});
			
			$('#submit_info').click(function() {
				$('#info_form').submit();
				return false;
			});
			
			$('#info_form').submit(function(){
				var fields = $(this).serializeArray();
				$.each(fields, function(i, field){
					that.trail.set(field.name, field.value);
				});
				that.save_trail();
				that.rate_track();

				return false;
			});
		},
		
		
		/** save details in trail object and save it on the server. */
		save_trail: function(){
			//TODO: validate first
			this.trail.save();
		},
		
		/** update map */
		show_map: function(){
			$('#map_div').removeClass('hidden');
			this.mapview = new MapView({parent:"#mapdiv", geojson:this.trail.get("waypoints"), editable: true});
		},
		
		/** proceed to next view to allow creating UXC or UDH object and link it to this track. */
		rate_track: function(){
			console.log("rate trail");
			// destroy this view and pass the trail object to the next view?
			view = new RatingView(this.trail);
			this.remove();
		}
			
	});
	
	return TrailUploadView;
	
});


