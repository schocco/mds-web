from apps.trails.gis_math import haversine
from django.contrib.gis.db.models.fields import LineStringField
from django.contrib.gis.db.models.manager import GeoManager
from django.db import models
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
        Ups and downs in between are not taken into account, so that circular
        courses will always be 0.
        A positive number means, that the end point is higher than the start point.
        Unit: meters
        '''
        if(self.has_waypoints() and self.waypoints.z is not None):
            return self.waypoints.z[-1] - self.waypoints.z[0]
        return 0
    
    def _get_altitude_sections(self):
        '''
        returns a list of altitude differences with
        one element for each pair of consequent waypoints.
        
        A positive number means, that the end point is higher than the start point.
        Unit: meters
        '''
        if not self.has_waypoints() or self.waypoints.z is None:
            return []
        dest = self.waypoints.z[0]
        altitudes = []
        for altitude in self.waypoints.z[1:]:
            start = dest
            dest = altitude
            altitudes.append(dest-start)
        return altitudes
    
    def _get_length_sections(self):
        '''
        returns a list of distances with
        one element for each pair of consequent waypoints
        '''
        if not self.has_waypoints():
            return []
        length_sections = []
        destination = self.waypoints[0]
        for point in self.waypoints[1:]:
            origin = destination
            destination = point
            length_sections.append(haversine(origin[:2], destination[:2])) # ignore z
        return length_sections
    
    def _get_slope_sections(self):
        '''
        returns a list of slopes with
        one element for each pair of consequent waypoints.
        
        A positive number indicates uphill, a negative one downhill.
        '''
        if not self.has_waypoints():
            return []
        slopes = []
        altitudes = self._get_altitude_sections()
        lengths = self._get_length_sections()
        for idx, length in enumerate(lengths):
            alt = altitudes[idx]
            slopes.append(float(alt) / length / 10) # /1000 (length in km) * 100 (%)
        return slopes
    
    def get_max_slope(self, dh=None, uh=None):
        '''
        Calculates the slope in % for each pair of waypoints and returns
        the highest slope found.
        By default returns the maximum slope, be it uphill or downhill.
        
        The slope is always returned as a positive number.
        
        parameters:
         dh: set to true to get the maximum downhill slope
         uh: set to True to get the maximum uphill slope
        '''
        if(not self.has_waypoints()):
            return 0
        if(dh is uh):
            slopes = [abs(s) for s in self._get_slope_sections()]
            return max(slopes)
        elif(dh):
            return abs(min(self._get_slope_sections()))
        elif(uh):
            return max(self._get_slope_sections())
        
    def get_avg_slope(self):
        '''
        Calculates the average slope by dividing total altitude difference
        through the length of the track.
        
        Positive number indicates uphill, negative indicates downhill.
        '''
        if(self.has_waypoints()):
            return self.get_altitude_difference() / self.get_length() / 10
        return 0
        
     
    def get_length(self):
        '''
        Calculates the length of the track by measuring distances between
        each pair of waypoints.
        
        Uses the Haversine Formula,
        see http://www.movable-type.co.uk/scripts/gis-faq-5.1.html
        '''        
        lengths = self._get_length_sections()
        return sum(lengths)
        
    def get_total_ascent(self):
        '''
        Calculates the total uphill meters (altitude).
        Returns the absolute value.
        '''
        total = 0
        for alt in self._get_altitude_sections():
            if alt > 0:
                total += alt
        return abs(total)
        
    def get_total_descent(self):
        '''
        Calculates the total downhill meters (altitude)
        Returns the absolute value.
        '''
        total = 0
        for alt in self._get_altitude_sections():
            if alt < 0:
                total += alt
        return abs(total)
    
    def fetch_altitude_info(self, datasource="OSM"):
        '''
        replace z values with data from 3rd party provider
        as specified in source
        '''
        #TODO
        raise NotImplementedError("not possible yet.")
