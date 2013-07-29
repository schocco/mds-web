from django.contrib.gis.db.models.fields import PointField, LineStringField
from django.contrib.gis.db.models.manager import GeoManager
from django.db import models, models
from django.utils.translation import ugettext_lazy as _



class Trail(models.Model):
    '''
    Representation of a muni track.
    '''
    name = models.CharField(max_length=100)
    created = models.DateTimeField()
    edited = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True)
    waypoints = LineStringField()
    objects = GeoManager()
    # user
    # comments[]
    # country
    # unitours link
    # pictures[]
    
    def __unicode__(self):
        return u'%s' % self.name
    
#class WayPoint(models.Model):
#    '''
#    A gpx waypoint.
#    '''
#    geometry = PointField(srid=4326)
#    trail = models.ForeignKey(Trail)
#    objects = GeoManager()
#    
#    def __unicode__(self):
#        return u'%s %s %s' % (self.trail, self.geometry.x, self.geometry.y)