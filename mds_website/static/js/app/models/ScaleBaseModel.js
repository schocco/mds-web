/**
 * A base model for the scales (UDH and UXC) with some common logic for retrieval and validation.
 */

define(['backbone'],
		function(Backbone){
	var BaseModel = Backbone.Model.extend({
		
		/** retrieve the score for the current values without saving the object. */
		get_score: function(){
			var uri = this.urlRoot + "calculate/";
			result = {};
			var that = this;
			var jqxhr = $.post(uri, this.attributes,
				function(data) { 
					that.set("score", data);
					console.log("Updated score for " + that);
					that.trigger("score_update");
				})
				.fail(function(data) {
					console.log("updating score for " + that + "failed");
					that.trigger("score_update", data);
					console.log(data);
				});
		}
	
	});
	return BaseModel;
	
});


