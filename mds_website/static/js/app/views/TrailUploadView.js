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
					//status.html(xhr.responseText);
					that.trail.set({waypoints: JSON.parse(xhr.responseText)});
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
				var data = $(this).serializeArray();
				console.log(data);
				that.trail.set("name", data[0].value);
				that.trail.set("description", data[1].value);
				that.save_trail();
				return false;
			});
		},
		
		
		/** save details in trail object and save it on the server. */
		save_trail: function(){
			this.trail.save();
		},
		
		
		/** update map */
		show_map: function(){
			this.mapview = new MapView({parent:"#mapdiv", geojson:this.trail.get("waypoints"), editable: true});
		}
			
	});
	
	return TrailUploadView;
	
});


