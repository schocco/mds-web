define(['models/BaseModel'],
		function(BaseModel){
	var SocialAuthBackend = BaseModel.extend({
		
		prefix: "/login/",
		urlRoot: "/api/v1/socialauth_backends/",
		
		map: {
                facebook: ["facebook", "icon-facebook", "facebook"],
                "google-oauth2": ["google", "icon-googleplus", "google"],
                twitter: ["twitter", "icon-twitter", "twitter"],               
        },
		
		get_url: function(){
			return this.prefix + this.get('name') + "/";
		},
		
		/**
		 * Return the icon class name.
		 */
		getIconClass: function(){

		    return this.map[this.get('name')][1];
		},
		
		 /**
         * Return the color class name
         */
        getColorClass: function(){
            return this.map[this.get('name')][2];
        },
        
        getDisplayName: function(){
            return this.map[this.get('name')][0];
        }
	
	});
	return SocialAuthBackend;
	
});


