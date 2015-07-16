from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized


class TrailAuthorization(DjangoAuthorization):
    '''
    Authorization class for the trails resource.
    
    Always allow read access.
    Allow creates for authenticated users.
    Restrict modifications and deletes to owned resources.
    '''
    def read_list(self, object_list, bundle):
        'Always allowed.'
        return object_list

    def read_detail(self, object_list, bundle):
        'Always allowed.'
        return True
    
    def create_detail(self, object_list, bundle):
        'only allowed if user matches'
        has_permission = super(TrailAuthorization, self).create_detail(object_list, bundle)
        return has_permission and bundle.obj.owner == bundle.request.user

    def update_list(self, object_list, bundle):
        'only allowed for owned objects'
        allowed = super(TrailAuthorization, self).update_list(object_list, bundle)
        owned = []
        for obj in allowed:
            if obj.owner == bundle.request.user:
                owned.append(obj)
        return owned

    def update_detail(self, object_list, bundle):
        'only allowed if user matches'
        has_permission = super(TrailAuthorization, self).update_detail(object_list, bundle)
        return has_permission and bundle.obj.owner == bundle.request.user

    def delete_list(self, object_list, bundle):
        'deletes are only allowed for single objects'
        raise Unauthorized("Only individual deletes are allowed.")

    def delete_detail(self, object_list, bundle):
        has_permission = super(TrailAuthorization, self).delete_detail(object_list, bundle)
        return has_permission and bundle.obj.owner == bundle.request.user
