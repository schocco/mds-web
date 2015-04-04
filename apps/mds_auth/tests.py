from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase

from apps.mds_auth.permissions import DEFAULT_GROUP_NAME, \
    get_or_create_default_group


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
