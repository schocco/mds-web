from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group, Permission
import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory
from django.utils.encoding import force_text
from social.apps.django_app.default.models import UserSocialAuth
from tastypie.serializers import Serializer
from tastypie.test import ResourceTestCase
from apps.mds_auth.authentication import OAuth20Authentication
import datetime as dt

from apps.mds_auth.permissions import DEFAULT_GROUP_NAME, \
    get_or_create_default_group

class SessionAuthMixin(object):
    """
    Mixin for logging in and out using the django/tastypie session auth.
    """
    def login(self, username, password, client=None):
        login_url = reverse('api_login', kwargs={'resource_name':'users', 'api_name':'v1'})
        credentials = {"username": username, "password": password}
        resp = None
        if type(client) is Client:
            serializer = Serializer()
            data = serializer.to_json(credentials)
            resp = client.post(login_url, data=data, content_type="application/json")
        else:
            resp = self.api_client.post(login_url, format="json", data=credentials)
        return resp

    def logout(self):
        logout_url = reverse('api_logout', kwargs={'resource_name':'users', 'api_name':'v1'})
        resp = self.api_client.post(logout_url, format="json")
        return resp



class DjangoAuthTest(ResourceTestCase, SessionAuthMixin):
    """
    Tests logging in and out using the django session authentication via the tastypie API.
    """

    def setUp(self):
        super(DjangoAuthTest, self).setUp()

        # Create a user.
        self.username = 'user'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'user@example.com', self.password)

    def test_login(self):
        resp = self.login(self.username, self.password)
        self.assertValidJSONResponse(resp)
        self.assertTrue(resp.cookies.has_key("csrftoken"))
        self.assertTrue(resp.cookies.has_key("sessionid"))

    def test_login_invalid(self):
        resp = self.login("user", "invalid")
        self.assertHttpUnauthorized(resp)
        self.assertValidJSON(resp.content)

    def test_logout(self):
        self.login(self.username, self.password)
        self.assertValidJSONResponse(self.logout())
        # unauthenticated logout returns 401
        self.assertHttpUnauthorized(self.logout())


class AuthPermissionTestCase(TestCase):
    
    def test_default_permissions(self):
        '''newly created users should be associated with a default group.'''
        self.assertEqual(0, Group.objects.filter(name=DEFAULT_GROUP_NAME).count(),
                         "default group should not exist yet)")
        user = User.objects.create(username="testUser", password="hjd9724rg")
        self.assertEqual(1, Group.objects.filter(name=DEFAULT_GROUP_NAME).count(),
                         "default group should have been created")
        self.assertEqual(1, user.groups.filter(name=DEFAULT_GROUP_NAME).count(),
                         "user should now be inside the default group")
        
    def test_permission_count(self):
        '''
        Ensure that the default group is reviewed when the number of permissions changes.
        This can happen when custom permissions are added to one of the models.
        These custom permissions might not be appropriate for the default group.
        '''
        group = get_or_create_default_group()
        self.assertEqual(9, group.permissions.all().count(),
                         "The number of permissions has changed. Please review the "
                         + "default group, are there any permissions which shouldn't be there?")


class Oauth20AuthenticationTestCase(ResourceTestCase):
    """
    Checks if the oauth authentication class correctly detects users based on the authorization header.
    """

    def setUp(self):
        """
        Creates users and associations with access tokens in extra data.
        :return:
        """
        super(Oauth20AuthenticationTestCase, self).setUp()
        self.user_logged_in = User.objects.create_user("username", 'user@example.com', "userpass", last_login = dt.datetime.now())
        authenticate(username="username", password="userpass")
        self.user_logged_out = User.objects.create_user("out", 'out@example.com', "userpass")
        self.token_logged_in = "CAACp6Me1lPUBAA9wZntrlubazxSWoiJZC3zmO3zD5xHaCU0tTpk4PyOv2ZCAmEMNOsWBXooWwp1w0dWOnnZC"
        self.token_logged_out = "cfghCp6Muzriewzirzeiru89w7rz8wghrh89zhoia87zhadkjahd977udhaiuhd7a9zdahd98qhdzauihd987"
        extra_data1 = json.dumps({"access_token": self.token_logged_in, "other_field": "extradata"})
        extra_data2 = json.dumps({"access_token": self.token_logged_out})
        UserSocialAuth.objects.create(extra_data = extra_data1, user = self.user_logged_in, uid=1)
        UserSocialAuth.objects.create(extra_data = extra_data2, user = self.user_logged_out, uid=2)

    def test_authenticated(self):
        """
        The authentication class should return true when the user identified by the access token has a valid session.
        """
        authentication = OAuth20Authentication()
        request = RequestFactory().get("/api/v1/something", secure=True)
        request.META['HTTP_AUTHORIZATION'] = "bearer " + self.token_logged_in
        status = authentication.is_authenticated(request)
        self.assertTrue(status)

    def test_unauthenticated(self):
        """
        The authentication class should return false when the user identified by the access token is not logged in.
        """
        authentication = OAuth20Authentication()
        request = RequestFactory().get("/api/v1/something", secure=True)
        request.META['HTTP_AUTHORIZATION'] = "BEARer " + self.token_logged_out
        status = authentication.is_authenticated(request)
        self.assertFalse(status)

    def test_no_token(self):
        """
        A HttpUnauthorized response should be returned when no user matches the token or when the token is
        not present.
        """
        authentication = OAuth20Authentication()
        # invalid token
        request = RequestFactory().get("/api/v1/something", secure=True)
        request.META['HTTP_AUTHORIZATION'] = "bearer invalidtoken"
        status = authentication.is_authenticated(request)
        self.assertHttpUnauthorized(status)
        # no token
        request = RequestFactory().get("/api/v1/something", secure=True)
        status = authentication.is_authenticated(request)
        self.assertHttpUnauthorized(status)

    def test_api_call_authenticated(self):
        """
        Authorized clients should get the proper result when checking their current auth status using the oauth token.
        """
        auth_header_val = "bearer " + self.token_logged_in
        resp = self.api_client.get(reverse("api_auth-status", kwargs={'resource_name':'users', 'api_name':'v1'}), authentication=auth_header_val)
        self.assertValidJSONResponse(resp)
        data = json.loads(force_text(resp.content))
        self.assertEqual(data.get("status"), "loggedin")

    def test_api_call_unauthenticated(self):
        """
        Unauthorized lients should get the proper result when checking their current auth status using the oauth token.
        """
        auth_header_val = "bearer " + self.token_logged_out
        resp = self.api_client.get(reverse("api_auth-status", kwargs={'resource_name':'users', 'api_name':'v1'}), authentication=auth_header_val)
        self.assertValidJSONResponse(resp)
        data = json.loads(force_text(resp.content))
        self.assertEqual(data.get("status"), "loggedout")
