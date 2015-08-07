from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.authentication import SessionAuthentication
from apps.mds_auth.authentication import OAuth20Authentication


class ReadAllSessionAuthentication(SessionAuthentication):
    '''
    Authenticates every request as long as it is a get operation.
    Uses the default session Authentication otherwise.
    '''
    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return True
        return super(ReadAllSessionAuthentication, self).is_authenticated(request, **kwargs)

class ReadAllTokenAuthentication(OAuth20Authentication):
    '''
    Authenticates every request as long as it is a get operation.
    Uses the default session Authentication otherwise.
    '''
    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return True
        return super(ReadAllTokenAuthentication, self).is_authenticated(request, **kwargs)


class ReadAllDjangoAuthorization(DjangoAuthorization):
    '''
    Django Authorization which allows read access to all 
    resources but limits other requests to the granted
    permissions of the user model.
    '''
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True


class UserObjectsOnlyAuthorization(Authorization):
    '''
    Examplary custom authorization from the tastypie docs:
    http://django-tastypie.readthedocs.org/en/latest/authorization.html
    '''
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")