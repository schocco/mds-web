define([], function () {
  var collections = {};
  return {
	  collections: collections,
	  
	  /** return cached collection or fetch it if not present. */
	  get:	function(key, col, options){
		  if(!collections[key]){
			  collections[key] = new col();
			  collections[key].fetch(options);
		  } else if(options !== undefined && options.success){
		      options.success(collections[key]);
		  }
		  return collections[key];
	  },
	  
	  set: function(key, col){
		  collections[key] = col;
	  }
	  
  };
});