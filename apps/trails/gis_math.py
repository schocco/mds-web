import math

def haversine(origin, destination):
    '''
    :param origin: start position
    :param destination: end position
    
    .. See::
       http://www.movable-type.co.uk/scripts/gis-faq-5.1.html
    '''
    lat1, lon1 = origin
    lat2, lon2 = destination
    # Earth radius varies from 6356.752 km at the poles 
    # to 6378.137 km at the equator, use something in
    # between.
    radius = radius_for_lat(lat1) # km

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
    
    :return: radius for given latitude in km
    
    .. See::
       http://en.wikipedia.org/wiki/Earth_radius#Radius_at_a_given_geodetic_latitude
    '''
    maxr = 6378.137 # km
    minr = 6356.752 # km
    d = (minr**2 * math.cos(lat))**2 + (maxr**2 * math.sin(lat))**2
    div = (minr * math.cos(lat))**2 + (maxr * math.sin(lat))**2
    rlat = math.sqrt(d/div)
    return rlat
                