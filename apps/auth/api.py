# -*- coding: utf-8 -*-
'''
API that provides authentication information that would
usually be retrieved via template/context processors.
'''
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.models import User
from social.apps.django_app.utils import load_strategy
from social.backends import utils
from tastypie import fields
from tastypie.authentication import Authentication, SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.bundle import Bundle
from tastypie.exceptions import BadRequest
from tastypie.resources import BaseModelResource, ModelResource, Resource


class SocialSignUpResource(BaseModelResource):
    '''
    Resource to authenticate a user given his access token.
    '''

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['post']
        authentication = Authentication()
        authorization = Authorization()
        resource_name = "social_sign_up"

    def obj_create(self, bundle, request=None, **kwargs):
        provider = bundle.data['provider']
        access_token = bundle.data['access_token']

        strategy = load_strategy(backend=provider)
        user = strategy.backend.do_auth(access_token)
        if user and user.is_active:
            bundle.obj = user
            return bundle
        else:
            raise BadRequest("Error authenticating user with this provider")
        
class UserResource(ModelResource):
    'User profile and session information.'
    
    class Meta:
        #model = User
        queryset = User.objects.all()
        resource_name = 'user'
        list_allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        fields = ['username', 'email', 'last_login', 'first_name', 'last_name']
    
    def get_object_list(self, request): 
        return super(UserResource, self).get_object_list(request).filter(pk=request.user.pk)

        
 
class BackendResource(Resource):
    '''
    A read-only resource that lists all available social auth backends.
    '''
    name = fields.CharField(attribute='name')

    class Meta:
        resource_name = 'socialauth_backends'
        authorization = Authorization()
        allowed_methods = ['get']

        
    def apply_sorting(self, obj_list, options=None):
        """
        sorts by name (always ascending)
        """
        return sorted(obj_list, key=lambda m: m.name)

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['backend'] = bundle_or_obj.obj.name
        else:
            kwargs['backend'] = bundle_or_obj.name
        return kwargs

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<backend>[\w\d_.-]+)/$" %
                    self._meta.resource_name,
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def get_object_list(self, request):
        return utils.load_backends(settings.AUTHENTICATION_BACKENDS).values()

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        backend = kwargs['backend']
        return utils.load_backends(settings.AUTHENTICATION_BACKENDS)[backend]
   

    
