# coding=utf-8
"""
Middlewares to handle auth related exceptions.
See https://github.com/omab/python-social-auth/blob/master/social/exceptions.py for list of all exceptions
"""
from django.http import HttpResponse
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions
from social.exceptions import AuthCanceled


class SocialAuthExceptionHandlerMiddleware(SocialAuthExceptionMiddleware):
    """
    Handles exceptions from social auth.
    """
    def process_exception(self, request, exception):
        if type(exception) == AuthCanceled:
            #TODO: redirect to some meaningful view that tells the user to try again
            raise exception
        elif type(exception) == AuthAlreadyAssociated:
            #TODO: logout currently associated user and log in new user
            raise exception