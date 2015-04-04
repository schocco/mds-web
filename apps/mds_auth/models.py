from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from apps.mds_auth.permissions import set_permissions


class Profile(models.Model):
    'User profile'
    user = models.OneToOneField(User)
    gender = models.CharField(max_length="1",blank=True,null=True)
    facebook = models.CharField(max_length=200,blank=True,null=True)
    gplus = models.CharField(max_length=200,blank=True,null=True)
    # homebase/location

    def __unicode__(self):
        return u"%s's Profile" % self.user
    
# set permissions for new users
post_save.connect(set_permissions, sender=User)