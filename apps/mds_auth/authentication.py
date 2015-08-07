# coding=utf-8
import logging

from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from social.apps.django_app.default.models import UserSocialAuth

from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized


class OAuth20Authentication(Authentication):
    """
    Simple OAuth2.0 authentication backend which uses python social auths usersocialauth table to query for
    users with a matching oauth token.

    Assumes that clients obtain their tokens via this web service and not directly via the oauth providers. This ensures
    that signup is handled by the server and tokens are up to date and that clients won't expose any secrets or client
    ids.
    """
    def _unauthorized(self):
        return HttpUnauthorized()

    def is_authenticated(self, request, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return self._unauthorized()
        try:
            (auth_type, token) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type.lower() != 'bearer':
                return self._unauthorized()
            self.backend = request.META['oauth-backend']

        except:
            return self._unauthorized()

        try:
            auth_user = UserSocialAuth.objects.get(extra_data__contains='access_token="{0}"'.format(token))
            if auth_user.access_token != token: # in case someone managed to add such a string in another extra field
                return self._unauthorized
            user = auth_user.user
        except:
            return self._unauthorized()

        if user is None:
            return self._unauthorized()

        if not self.check_active(user) or not user.is_authenticated():
            return False
        else:
            request.user = user
            return True