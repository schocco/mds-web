define(['backbone',
        'models/TrailModel',
        'collections/TrailCollection',
        'cache',
        'views/_MapView',
        'views/TrailDetailView',
        'underscore',
        'text!templates/trail_upload.html',
        'views/BaseView',
        'jquery',
        'OpenLayers',
        'jquery-form'
        ],
		function(Backbone, Trail, TrailCollection, cache, MapView, TrailDetailView, _, tpl, BaseView, $, OpenLayers){
	
	var TrailUploadView = BaseView.extend({
		el: '#content',
		msg: '#upload_form_errors',
		title: 'Upload a trail',
//		events: {
//			""
//		},
		
		initialize: function () {
			BaseView.prototype.initialize.apply(this);
			var that = this;
		    var onDataHandler = function(collection) {
		    	console.log("fetched data.");
		        that.render();
		    };
			that.trail = new Trail();
			//the datahandler is only called when the collection is fetched the first time.
			that.collection = cache.get('TrailsCollection', TrailCollection, { success : onDataHandler });
			if(that.collection.length >= 0){
				that.render();
			}
			
   
		    
		},
		
		/** renders the whole view. */
		render: function(){
			console.log("render template");
			var that = this;
			var compiledTemplate = _.template(tpl)({type_choices: this.trail.type_choices});
			this.setContent(compiledTemplate);
			this.set_up_form();
		},
		
		/** add appropriate event handlers to the form */
		set_up_form: function(){
			
			var bar = $('.bar');
			var percent = $('.percent');
			var status = $('#status');
			var that = this;
			$('#upload_form').ajaxForm({
			    beforeSend: function(xhr, settings) {
			        status.empty();
			        var percentVal = '0%';
			        bar.width(percentVal);
			        percent.html(percentVal);
			    },
			    url: that.trail.urlRoot + "load-gpx/",
			    dataType: "json",
			    uploadProgress: function(event, position, total, percentComplete) {
			        var percentVal = percentComplete + '%';
			        bar.width(percentVal);
			        percent.html(percentVal);
			    },
			    success: function() {
			        var percentVal = '100%';
			        bar.width(percentVal);
			        percent.html(percentVal);
			    },
				complete: function(xhr) {
					if(xhr.status != 200){
						that.showMessage({msg:xhr.responseText, type:that.ERROR});
					} else {
						// poll for result and update trail if successful
						task_id = JSON.parse(xhr.responseText).task_id;
						//that.pollForResult(task_id);
						that.pollForResult(task_id);
						var path = $("#gpx").val();
						var fileName = String(path.match(/[^\/\\]+$/));
						fileName = fileName.slice(0, -4); //strip .gpx
						$("#name_field").val(fileName);
						// toggle visibility
						$('#import_div').addClass("hidden");
						$('#info_div').removeClass('hidden');
						$('#map_div').removeClass('hidden');
						// errors will be displayed in other div (other form)
						that.msg = '#info_form_errors';
					}
				}
			});

			//trigger submit when upload link is clicked
			$('#submit').click(function(e) {
				e.preventDefault();
				$('#upload_form').submit();
				that.hideMessage();
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
				that.hideMessage();
				that.save_trail();
				return false;
			});
		},
		
		pollForResult: function(task_id){
			var url = this.trail.urlRoot + "load-gpx/result/" + task_id + "/";
			var that = this;
			var xhr = $.getJSON(url)
				.done(function(data, textStatus, xhr){
					if(xhr.status == 204){
						console.log("try again");
						setTimeout(function() {
							that.pollForResult(task_id);
						}, 400);
					} else if(xhr.status == 200){
						that.trail.set({waypoints: data});
						that.show_map();
					}
				})
				.fail(function(xhr){
					that.showMessage({msg:xhr.responseJSON.error, type:that.ERROR});
				});
		},
		

		/** save details in trail object and save it on the server. */
		save_trail: function(){
			//TODO: validate first
			var that = this;
			that.collection.create(this.trail, {
				wait:true,
			    success:function(model, response) {
			        that.rate_track();
			    },
			    error: function(model, error) {
			    	that.showMessage({type:that.ERROR,msg:"Trail could not be saved."});
			        console.log(model.toJSON());
			    }
			});
		},
		
		/** update map */
		show_map: function(){
			this.mapview = new MapView({parent:"#mapdiv", geojson:this.trail.get("waypoints"), editable: true});
		},
		
		/** proceed to next view to allow creating UXC or UDH object and link it to this track. */
		rate_track: function(){
			this.goTo(this.trail.get_url());
		}
			
	});
	
	return TrailUploadView;
	
});


