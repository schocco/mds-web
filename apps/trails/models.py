from django.contrib.gis.db.models.fields import LineStringField
from django.contrib.gis.db.models.manager import GeoManager
from django.db import models, models
from django.utils.translation import ugettext_lazy as _



class Trail(models.Model):
    '''
    Representation of a muni track.
    '''
    name = models.CharField(_('name'), max_length=100)
    created = models.DateTimeField(_('created'), auto_now_add=True, blank=True)
    edited = models.DateTimeField(_('last change'), auto_now=True, blank=True)
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
    
    def has_waypoints(self):
        return self.waypoints is not None
    
    def get_altitude_difference(self):
        '''
        Calculates the total altitude difference between start and end point.
        Ignores ups and downs in between.
        '''
        #TODO
        
    def get_max_slope(self):
        '''
        Calculates the slope in % for each pair of waypoints and returns
        the highest slope found.
        '''
        
    def get_avg_slope(self):
        '''
        Calculates the average slope by dividing total altitude difference
        through the length of the track.
        '''
        
    def get_length(self):
        '''
        Calculates the (flat) distance of the track.
        This does not take into account that the earth isn't flat, and that
        the distance should be longer due to the altitude difference.
        '''
        
    def get_exact_length(self):
        '''
        Calculates the length of the track and takes into account that
        the earth is not flat + altitude difference.
        '''
        
    def get_total_altitude_up(self):
        '''
        Calculates the total uphill meters (altitude)
        '''
        #TODO
        
    def get_total_altitude_down(self):
        '''
        Calculates the total downhill meters (altitude)
        '''
        #TODO
        
