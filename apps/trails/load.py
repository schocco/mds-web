'''
module for gpx conversion tasks
'''
from apps.trails.models import Trail
from django.contrib.gis.utils import LayerMapping
import os



class GPXMapping(LayerMapping):
    '''
    3d Layer Mapping.
    
    Assuming a Django model with a LineString field called 'waypoints' and a
    GPX file test.gpx this class can be used as follows:
    
    track_mapping = {'waypoints' : 'LINESTRING'}
    gpx_file = 'test.gpx'

    lm = GPXMapping(Trail, gpx_file, track_mapping, layer=1)
    lm.save(verbose=True)
    '''
    # Snippet taken from http://djangosnippets.org/snippets/1800/
    def __init__(self, *args, **kwargs):
        # Setting this environment variable tells OGR to use the elevation
        # attribute as the Z coordinate value on the geometries.  See:
        #  http://www.gdal.org/ogr/drv_gpx.html
        os.environ['GPX_ELE_AS_25D'] = 'YES'
        super(GPXMapping, self).__init__(*args, **kwargs)
        # Unset the environment variable, so it doesn't affect other
        # GPX DataSource objects.
        os.environ.pop('GPX_ELE_AS_25D')
        
        
