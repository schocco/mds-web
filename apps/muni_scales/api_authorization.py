from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized


class UXXAuthorization(DjangoAuthorization):
    '''
    Authorization class for UDH and UXC resources.
    
    Always allow read access.
    Allow create/update/delete for authenticated users who are owners of the associated trail object.
    Additionally checks django permissions.
    '''
    def read_list(self, object_list, bundle):
        'Always allowed.'
        return object_list

    def read_detail(self, object_list, bundle):
        'Always allowed.'
        return True
    
    def create_detail(self, object_list, bundle):
        'only allowed if user matches'
        has_permission = super(UXXAuthorization, self).create_detail(object_list, bundle)
        return has_permission and bundle.obj.trail.owner == bundle.request.user

    def update_list(self, object_list, bundle):
        'only allowed for owned objects'
        allowed = super(UXXAuthorization, self).update_list(object_list, bundle)
        owned = []
        for obj in allowed:
            if obj.trail.owner == bundle.request.user:
                owned.append(obj)
        return owned

    def update_detail(self, object_list, bundle):
        'only allowed if user matches and has permission to update.'
        has_permission = super(UXXAuthorization, self).update_detail(object_list, bundle)
        return has_permission and bundle.obj.trail.owner == bundle.request.user

    def delete_list(self, object_list, bundle):
        'deletes are only allowed for single objects'
        raise Unauthorized("Only individual deletes are allowed.")

    def delete_detail(self, object_list, bundle):
        has_permission = super(UXXAuthorization, self).delete_detail(object_list, bundle)
        return has_permission and bundle.obj.trail.owner == bundle.request.user
