from django.contrib.gis.db.models.fields import LineStringField
from django.contrib.gis.db.models.manager import GeoManager
from django.db import models, models
from django.utils.translation import ugettext_lazy as _



class Trail(models.Model):
    '''
    Representation of a muni track.
    '''
    name = models.CharField(_('name'), max_length=100)
    created = models.DateTimeField(_('created'))
    edited = models.DateTimeField(_('last change'),auto_now_add=True)
    description = models.CharField(_('description'), max_length=500, blank=True)
    waypoints = LineStringField(_('waypoints'), dim=3, null=True, blank=True) #include altitude as Z
    objects = GeoManager()
    # user
    # comments[]
    # country
    # unitours link
    # pictures[]
    
    def __unicode__(self):
        return u'%s' % self.name
