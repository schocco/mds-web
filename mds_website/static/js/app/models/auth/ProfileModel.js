define(['models/BaseModel'],
		function(BaseModel){
	var ProfileModel = BaseModel.extend({
		defaults: {
			user: null,
			username: "anonymous",
		},
		schema: {
            gender: { type: 'Select', options: ['', 'm', 'f'] },
            name:  'Text',
            birthday: 'Date'
        }
			
	}
	return ProfileModel;
});