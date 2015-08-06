# coding=utf-8
"""
Middlewares to handle auth related exceptions.
See https://github.com/omab/python-social-auth/blob/master/social/exceptions.py for list of all exceptions
"""
from django.http import HttpResponse, JsonResponse
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions
from social.exceptions import AuthCanceled, AuthAlreadyAssociated
from django.utils.translation import ugettext_lazy as _


class SocialAuthExceptionHandlerMiddleware(SocialAuthExceptionMiddleware):
    """
    Handles exceptions from social auth.
    """

    def process_exception(self, request, exception):
        if type(exception) == AuthAlreadyAssociated:
            # this can happen when a user is already logged in via one backend (e.g. facebook)
            # and then tries to sign in via another one (e.g. google)
            # clients should check the session before trying to log in, but if they don't
            # provide a more meaningful error message
            response = JsonResponse({'error': _(
                'You are already logged in via another OAuth provider. '
                'Sign out first if you want to log in with another account.')})
            response.status_code = 400
            return response