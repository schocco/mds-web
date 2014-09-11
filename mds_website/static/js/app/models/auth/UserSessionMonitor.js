define(['models/auth/UserModel', 'module'],	function(UserModel, module){

	/** number of errors that occurred checking the session. */
	var errorCount = 0;
	
	/**
	 * Repeatedly check the current session. 
	 * Stop checking when the user logs out or 
	 * when the session is invalid.
	 */
	var doSessionCheck = function(){
		var that = this;
		var interval = module.config().interval; //time to wait between checks
		var maxRetries = module.config().maxRetries;
		
		var loggedInHandler = function(){
			// session valid, keep checking
			setTimeout(doSessionCheck, interval);
		};
		var loggedOutHandler = function(){
			// change current user to default (anonymous)
			var anonymous = new UserModel;
			UserModel.setCurrentUser(anonymous)
			// no more checking until logged in again
		};
		var errorHandler = function(){
			// increase error count
			// keep checking unless too many errors
			that.errorCount++;
			if(that.errorCount < maxRetries){
				setTimeout(that.doSessionCheck, interval);
			} else {
				that.loggedOutHandler();
				that.errorCount = 0;
			}
		}
		
		// only need to check when the session seems to be valid,
		// anything else is handled by events
		if(UserModel.currentUser.isAuthenticated()){
			UserModel.checkAuthStatus({
				loggedIn: loggedInHandler,
				loggedOut: loggedOutHandler,
				error: errorHandler});
		}

	};
	
	/**
	 * Periodically check if the users session has expired.
	 * Also listen for login and logout events to update the current user accordingly.
	 * Trigger an event when the currentUser has changed so that views depending on the current user can
	 * react to the change.
	 * Display a message to the user that the session has expired.
	 * Load interval for session checks from module config.
	 */
	var startMonitoring = function(){
		// set up event listeners
		UserModel.events.on("user_login", doSessionCheck, this);
		UserModel.events.on("user_logout", function(){
			var anonymous = new UserModel;
			UserModel.setCurrentUser(anonymous);
		}, this)
		// only start if user is logged in
		// otherwise just listen for login event and start monitoring after login occured
		if(UserModel.currentUser.isAuthenticated){
			doSessionCheck();
		}
		
	};
	
	return {
		start: startMonitoring
	}
	
	});