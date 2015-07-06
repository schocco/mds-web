from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized


class UXXAuthorization(DjangoAuthorization):
    '''
    Authorization class for UDH and UXC resources.
    
    Always allow read access.
    Allow creates for authenticated users who are owners of the associated trail object.
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
        #TODO: check superclass
        return bundle.obj.trail.owner == bundle.request.user

    def update_list(self, object_list, bundle):
        'only allowed for owned objects'
        allowed = [] #TODO: check superclass
        for obj in object_list:
            if obj.owner == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        'only allowed if user matches'
        return bundle.obj.owner == bundle.request.user

    def delete_list(self, object_list, bundle):
        'deletes are only allowed for single objects'
        raise Unauthorized("Only individual deletes are allowed.")

    def delete_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user
