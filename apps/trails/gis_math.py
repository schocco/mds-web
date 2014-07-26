from bisect import bisect
from django.contrib.gis.geos.point import Point
import math


def haversine(origin, destination):
    '''
    :param origin: start position
    :param destination: end position
    :return: length in meters
    
    .. See::
       http://www.movable-type.co.uk/scripts/gis-faq-5.1.html
    '''
    lat1, lon1 = origin
    lat2, lon2 = destination
    # Earth radius varies from 6356.752 km at the poles 
    # to 6378.137 km at the equator, use something in
    # between.
    radius = radius_for_lat(lat1) # m

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

def radius_for_lat(lat):
    '''
    Rt = radius of earth at latitude t                
    maxr = major radius of earth         = 6,378,137 meters
    minr = minor radius of earth         = 6,356,752.31420 meters 
    
    Rt= SQRT( (((minr^2cos(t))^2)+((maxr^2sin(t))^2))/    ((acos(t))^2 + (maxr * sin(t)^2))
    
    :return: radius for given latitude in m
    
    .. See::
       http://en.wikipedia.org/wiki/Earth_radius#Radius_at_a_given_geodetic_latitude
    '''
    maxr = 6378137.0 # m
    minr = 6356752.0 # m
    d = (minr**2 * math.cos(lat))**2 + (maxr**2 * math.sin(lat))**2
    div = (minr * math.cos(lat))**2 + (maxr * math.sin(lat))**2
    rlat = math.sqrt(d/div)
    return rlat


class RasterRow:
    
    def __init__(self):
        self.length_degree = 0
        self.length_meters = 0
        self.length_degree_cum = 0
        self.length_meters_cum = 0
        self.altitude = 0
        self.slope = 0


class RasterMap:
    '''
    Class to calculate approximated information about a trail object.
    '''
    def __init__(self, trail):
        #flatten multilinestring to linestring
        self.linestring = [point for linestring in trail.waypoints for point in linestring]
        self.length = trail.waypoints.length
        self.length_m = trail.trail_length or 0
        self.rasterRows = []
        self.distances = [] #4th dimension of linestring with cumulative distance to the start point
        
        
        self.build()
        self.raster()
        
    def build(self):
        #calculate distance at each point in the linestring
        b = Point(self.linestring[0])
        distance_cum = 0
        for p in self.linestring:
            a = b
            b = Point(p)
            distance = a.distance(b)
            distance_cum += distance
            self.distances.append(distance_cum)
            
    def raster(self):
        '''
        Divide a track into equally long sections and get the altitude at each point.
        According to the MDS document a section is a part of the track of 5-20 meters.
        '''
        # the size of the segments should be chosen so that the calculation effort is not too cpu intensive
        steps = 0
        if self.length_m <= 1000:
            #5m is the minimum section length according to the mds document
            steps = self.length_m/5
        elif self.length_m > 30000:
            #50m segments for tracks longer than 30km
            steps = self.length_m/50
        elif self.length_m > 1000:
            # use 20m segments for tracks between 1 and 30km
            steps = self.length_m/20
        
        row = None

        for step in range(int(steps)):
            prev_row = row
            row = RasterRow()
            row.length_degree = self.length / steps
            row.length_degree_cum = row.length_degree * step
            row.length_meters = self.length_m / steps
            row.length_meters_cum = row.length_meters * step
            if(row.length_degree_cum in self.distances):
                row.altitude = self.linestring[self.distances.index(row.length_degree_cum)][2]
            else:
                # get index of element closest to the needed value
                right_idx = bisect(self.distances, row.length_degree_cum)
                # distances[i] is lower than the value, so i+1 is the right neighbour
                left_idx = right_idx - 1

                if(right_idx >= len(self.linestring)):
                    # the right index can be out of range
                    # in that case we can simply use the last value instead of interpolating
                    row.altitude = self.linestring[-1][2]
                else:
                    # now interpolate
                    h0 = self.linestring[left_idx][2]
                    h1 = self.linestring[right_idx][2]
                    x0 = self.distances[left_idx]
                    x1 = self.distances[right_idx]
                    row.altitude = h0 + (h1-h0)/(x1-x0) * (row.length_degree_cum - x0)
            self.rasterRows.append(row)
            if(prev_row is not None and row.length_meters != 0):
                row.slope = float((row.altitude - prev_row.altitude)/row.length_meters)