import math

def haversine(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    # Earth radius varies from 6356.752 km at the poles 
    # to 6378.137 km at the equator, use something in
    # between
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d