define(['backbone',
        'models/TrailModel',
        'views/_MapView',
        'underscore',
        'text!templates/trail_upload.html',
        'jquery',
        'openlayers',
        'jquery_form'],
		function(Backbone, Trail, MapView, _, tpl, $, OpenLayers){
	
	var TrailUploadView = Backbone.View.extend({
		el: '#content',		
		
		initialize: function () {
			var that = this;
			that.render();
		    that.trail = new Trail();
   
		    
		},
		
		/** renders the whole view. */
		render: function(){
			console.log("render template");
			var compiledTemplate = _.template(tpl);
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
					status.html(xhr.responseText);
					console.log("xhr " + JSON.parse(xhr.responseText));
					that.trail.set({waypoints: JSON.parse(xhr.responseText)});
					console.log(that.trail);
					that.show_map();
				}
			}); 

			//trigger submit when upload link is clicked
			$('#submit').click(function() {
				$('#upload_form').submit();
				return false;
			});
		},
		
		
		/** update map */
		show_map: function(){
			if(this.mapview){
				console.log("there is already a map instance.");
				//this.mapview = null;
				//$("#mapdiv").empty();
			}
			this.mapview = new MapView({parent:"#mapdiv", geojson:this.trail.get("waypoints")});
		}
			
	});
	
	return TrailUploadView;
	
});


