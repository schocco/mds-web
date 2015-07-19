from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from apps.mds_auth.permissions import set_permissions
from apps.muni_scales.models import UXCscale, UDHscale
from apps.trails.models import Trail



class Profile(models.Model):
    """User profile"""
    user = models.OneToOneField(User)
    tagline = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length="1", blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    gplus = models.CharField(max_length=200, blank=True, null=True)
    #picture = models.ImageField(upload_to="profiles", blank=True, null=True)
    #country = CountryField(blank=True, null=True)
    #city

    def __unicode__(self):
        return u"%s's Profile" % self.user

    def get_num_uploaded(self):
        """

        :return: the number of uploaded trails
        """
        return Trail.objects.filter(owner=self.user).count()

    def get_num_rated(self):
        """

        :return: the number of rated trails
        """
        return UDHscale.objects.filter(trail__owner=self.user).count() + UXCscale.objects.filter(trail__owner=self.user).count()


# set permissions for new users
post_save.connect(set_permissions, sender=User)