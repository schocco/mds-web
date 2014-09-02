
define(['backbone',
        'underscore',
        'jquery'],
		function(Backbone, _, $){
	
	
	var MessageMixin = {
			//the view has to define a msg field
//			//CONSTANTS, (accessible via MessageMixin.CONSTANT
			INFO : "INFO",
			WARNING: "WARNING",
			ERROR: "ERROR",
		
		
		/**
		 * Display the message.
		 * @param type (MessageMixin.INFO|WARNING|ERROR)
		 * @param msg message to be displayed, either a string or an array.
		 */
		showMessage: function (options) {
			var type = options.type;
			var message = options.msg;
			var content;
			var msgEl = $(this.msg);
			
			// set appropriate styles
			if(type == MessageMixin.INFO){
				msgEl.attr("class","alert alert-info");
			} else if (type == MessageMixin.WARNING){
				msgEl.attr("class","alert alert-warning");
			} else if (type == MessageMixin.ERROR){
				msgEl.attr("class","alert alert-error");
			}
						
			
			if(_.isString(message)){
				content = message;
			} else if(_.isArray(message)){
				var tpl = "<ul><% _.each(errors, function(err) { %><li><%= err %></li><% }); %></ul>";
				content = _.template(tpl, {errors: errors});
			} else {
				throw "Unexpected input: need string or array to display message.";
			}
			msgEl.html(content);
			msgEl.show({duration: 300});
		},
		
		/**
		 * Hide the message again.
		 */
		hideMessage: function () {
			$(this.msg).html("");
			$(this.msg).hide({duration:100});
		}
		
			
	};
	
	
	return MessageMixin;
	
});


