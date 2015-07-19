from django.contrib.auth.models import User, Group, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from tastypie.test import ResourceTestCase

from apps.mds_auth.permissions import DEFAULT_GROUP_NAME, \
    get_or_create_default_group

class SessionAuthMixin(object):
    """
    Mixin for logging in and out using the django/tastypie session auth.
    """
    def login(self, username, password):
        login_url = reverse('api_login', kwargs={'resource_name':'users', 'api_name':'v1'})
        credentials = {"username": username, "password": password}
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
