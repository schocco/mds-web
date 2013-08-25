define(['backbone'],
		function(Backbone){
	var BaseModel = Backbone.Model.extend({
		
		prefix: "#/",
		
		url: function() {
			var origUrl = Backbone.Model.prototype.url.call(this);
			return origUrl + (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
		},
		
		get_url: function(){
			return this.prefix + this.get('id');
		}
	
	});
	return BaseModel;
	
});


