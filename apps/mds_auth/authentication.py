# coding=utf-8
from social.apps.django_app.default.models import UserSocialAuth
import logging
from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized
import pytz
import datetime as dt
from django.conf import settings

logger = logging.getLogger(__name__)

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

    @staticmethod
    def _expired(user):
        """
        Calculates the difference between now and the last login time of the user.
        If the difference is higher than the maximum duration, the user is considered unauthenticated.

        :return: true if the last login is was within the maximum session time
        """
        oauth_session_length = getattr(settings, "OAUTH_SESSION_TIMEOUT", 12 * 60 * 60)
        use_tz = getattr(settings, "USE_TZ", False)

        try:
            now = dt.datetime.now()
            if use_tz:
                now = pytz.utc.localize(now)
            delta_seconds = (now - user.last_login).total_seconds()
            if delta_seconds > oauth_session_length:
                logger.debug("user's last login is too long ago, session expired")
                return True
            else:
                logger.debug("user session still active")
                return False
        except Exception, e:
            logger.debug("error checking last login time" + str(e))
            return True



    def is_authenticated(self, request, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return self._unauthorized()
        try:
            (auth_type, token) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type.lower() != 'bearer':
                logger.debug("Expected 'bearer' type but got {0}".format(auth_type))
                return self._unauthorized()
        except Exception, e:
            logger.debug("no valid authorization header found", e)
            return self._unauthorized()

        try:
            auth_user = UserSocialAuth.objects.get(extra_data__contains='"access_token": "{0}"'.format(token))
            if auth_user.access_token != token:  # in case someone managed to add such a string in another extra field
                logger.warn("the query for a user returned a result, but the user's token differs from the lookup token.")
                return self._unauthorized
            user = auth_user.user
        except Exception, e:
            logger.debug("No social auth user object found for this token")
            return self._unauthorized()

        if user is None:
            logger.debug("User is None -> unauthorized")
            return self._unauthorized()

        if self.check_active(user) and not self._expired(user):
            logger.debug("user is active and session is still valid")
            request.user = user
            return True
        else:
            logger.debug("user inactive or session expired.")
            return False