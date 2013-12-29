from apps.trails.gis_math import haversine
from django.contrib.gis.db.models.fields import LineStringField, \
    MultiLineStringField
from django.contrib.gis.db.models.manager import GeoManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

import logging
logger = logging.getLogger(__name__)

TRAIL_TYPE_CHOICES = (
                      ("unknown", _("unknown")),
                      ("uphill", _("uphill")),
                      ("downhill", _("downhill")),
                      ("xc", _("cross country")),                      
                      )

class Trail(models.Model):
    '''
    Representation of a muni track.
    '''
    name = models.CharField(_('name'), max_length=100, blank=False)
    type = models.CharField(_('trail type'), choices = TRAIL_TYPE_CHOICES, max_length=100)
    created = models.DateTimeField(_('created'), auto_now_add=True, blank=True)
    edited = models.DateTimeField(_('last change'), auto_now=True, blank=True)
    description = models.CharField(_('description'), max_length=500, blank=True)
    waypoints = MultiLineStringField(_('waypoints'), dim=3, null=True, blank=True) #include altitude as Z
    trail_length = models.IntegerField(_('length'), help_text=_("in meters"), blank=True, null=True)
    objects = GeoManager()
    # user
    # comments[]
    # country
    # unitours link
    # pictures[]
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def _generator(self):
        '''
        Yields 1 once, and then 0 for all subsequent calls.
        
        This can be used for loops where the first element in the first linestring
        needs to be treated differently than all other linestring elements in the 
        multilinestring.
        '''
        yield 1
        while(True):
            yield 0
    
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
        if(self.has_waypoints() and self.waypoints[0].z is not None):
            #last point in last linestring - first point in first linestring
            return self.waypoints[0].z[0] - self.waypoints[-1].z[-1]
        return 0
    
    def _get_altitude_sections(self):
        '''
        returns a list of altitude differences with
        one element for each pair of consequent waypoints.
        
        A positive number means, that the end point is higher than the start point.
        Unit: meters
        '''
        if not self.has_waypoints() or self.waypoints[0].z is None:
            return []
        altitudes = []
        dest = self.waypoints[0].z[0]
        idx = self._generator()
        for ls in self.waypoints:
            # exclude first element on first run, use all elements otherwise
            for altitude in ls.z[idx.next():]:
                start = dest
                dest = altitude
                altitudes.append(start-dest)
        return altitudes
    
    def _get_length_sections(self):
        '''
        :return: a list of distances in meters with
        one element for each pair of consequent waypoints
        '''
        if not self.has_waypoints():
            return []
        length_sections = []
        destination = self.waypoints[0][0]
        idx = self._generator()
        for linestring in self.waypoints:
            # exclude first element on first run, use all elements otherwise
            for point in linestring[idx.next():]:
                origin = destination
                destination = point
                length_sections.append(haversine(origin[:2], destination[:2])) # ignore z
        return length_sections
    
    def _flat_z(self):
        zs = []
        if not self.has_waypoints() or self.waypoints[0].z is None:
            return zs
        for ls in self.waypoints:
            zs = zs + ls.z
        return zs
    
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
        if(len(altitudes) == len(lengths)):
            for idx, length in enumerate(lengths):
                alt = altitudes[idx]
                try:
                    slopes.append(float(alt) / length * 100) # in %
                except ZeroDivisionError, e:
                    logger.error(e)
                    slopes.append(0)
        return slopes
    
    def get_max_slope(self, dh=None, uh=None):
        '''
        Calculates the slope in % for each pair of waypoints and returns
        the highest slope found.
        By default returns the maximum slope, be it uphill (positive number) or downhill (negative number).
        
        :param bool dh: set to True to get the maximum downhill slope
        :param bool uh: set to True to get the maximum uphill slope
        '''
        logger.debug("get max slope")
        
        sections = self._get_slope_sections()
        if(not self.has_waypoints() or len(sections) == 0):
            return 0
        if(dh is uh):
            if abs(min(sections)) > max(sections):
                return min(sections)
            else:
                return max(sections)
        elif(dh):
            return min(sections)
        elif(uh):
            return max(sections)
        
    def get_avg_slope(self):
        '''
        Calculates the average slope by dividing total altitude difference
        through the length of the track.
        
        :return: slope in %. Positive number indicates uphill, negative indicates downhill.
        '''
        logger.debug("get avg slope")
        if(self.has_waypoints()):
            return (self.get_altitude_difference() / self.get_length(unit="m")) * 100 # in %
        return 0
        
     
    def get_length(self, unit="m"):
        '''
        Calculates the length of the track by measuring distances between
        each pair of waypoints.
        
        Uses the Haversine Formula,
        see http://www.movable-type.co.uk/scripts/gis-faq-5.1.html
        
        :param str unit: unit to be returned (either "m" or "km")
        :return: the length in `unit`
        '''
        logger.debug("get length")
        if(self.has_waypoints()):
            lengths = self._get_length_sections()
            if unit == "km":
                return sum(lengths)/1000
            if unit == "m":
                return sum(lengths)
            else: raise ValueError("Only m or km are allowed.")
        return 0
        
    def get_total_ascent(self):
        '''
        Calculates the total uphill meters (altitude).
        
        :returns: the absolute value.
        '''
        logger.debug("get total ascent")
        total = 0
        for alt in self._get_altitude_sections():
            if alt > 0:
                total += alt
        return abs(total)
        
    def get_total_descent(self):
        '''
        Calculates the total downhill meters (altitude)
        
        :returns: the absolute value in meters
        '''
        logger.debug("get total descent")
        total = 0
        for alt in self._get_altitude_sections():
            if alt < 0:
                total += alt
        return abs(total)
    
    def get_height_at(self, meter):
        '''
        :param int meter: distance from the start point of the track in meters
        
        Return the approximate height at a given position of a track.
        Interpolates nearest waypoints to get the height in meters.
        '''
        lengths = self._get_length_sections()
        # it is necessary to get a flat list of all z values
        # to look up values that correspond to length sections
        zs = self._flat_z()
        # transform to cumulative lengths
        total = 0
        prev_total = 0
        for idx, section in enumerate(lengths):
            prev_total = total
            total += section
            lengths[idx] = int(total)
            # return z value of matching point if present
            if meter == int(total):
                return zs[idx]
            if meter > prev_total and meter < total:
                h0 = zs[idx-1]
                h1 = zs[idx]
                m0 = prev_total
                m1 = total                
                result = float(meter - m0) / (m1 - m0) * (h1 - h0) + h0
                return result
            
    
    def get_height_profile(self, scale_steps=20):
        '''
        :param int scale_steps: specifies how many 
        
        Creates a dictionary which contains height information
        along a dynamically set scale of distance points.
        Height for each point is calculated via interpolation using the nearest 2
        waypoints.
        '''
        logger.debug("get height profile")
        
        zs = self._flat_z()
        min_height = round(min(zs),1)
        max_height = round(max(zs),1)
        length = self.get_length(unit="km")

        step = length / scale_steps
        labels = ['0 km']
        values = [round(zs[0],1)]
        total = 0
        for i in range(scale_steps-2):
            total += step
            labels.append('%.1f km' % total)
            values.append(round(self.get_height_at(total*1000),1)) # total in meters
        labels.append('%.1f km' % length)
        values.append(round(zs[-1],1))
        
        height_profile = {'max_height': max_height,
                          'min_height': min_height,
                          'labels': labels,
                          'values': values}
        return height_profile
        
    
    def fetch_altitude_info(self, datasource="OSM"):
        '''
        replace z values with data from 3rd party provider
        as specified in source
        '''
        #TODO
        raise NotImplementedError("not possible yet.")
