'''
module for gpx conversion tasks
'''
import os

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.error import OGRException
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos.linestring import LineString
from osgeo import ogr



class GPXImportError(Exception):
    'Exception to be raised when gpx files cannot be read.'
    pass


class GPXReader(object):
    '''
    Utility class to extract waypoints, routes or tracks from gpx files.
    '''
    
    def __init__(self, file_path, dim3 = True):
        if(dim3):
            # tell OGR to use the elevation attribute as the Z coordinate
            # value on the geometries.  See: http://www.gdal.org/ogr/drv_gpx.html
            os.environ['GPX_ELE_AS_25D'] = 'YES'
        ogr.UseExceptions()
        self.gpx_file = file_path
        try:
            self.ds = DataSource(self.gpx_file)
        except OGRException, e:
            raise GPXImportError("Invalid data source.")
        # Unset the environment variable, so it doesn't affect other
        # GPX DataSource objects.
        if(dim3):
            os.environ.pop('GPX_ELE_AS_25D')
        
        if self.ds is None:
            raise GPXImportError("Cant use %s as datasource" % file_path)
    
    def _guess_layer(self):
        '''
        Guesses which layer contains the relevant trail data.
        It is most likely that the route or track layer contains the complete trail.
        If those are not present, it is checked whether there are enough waypoints
        that could make a complete trail.
        :return: index for the layer
        '''
        for layer_idx in (4,3):
            # layer 4 has all track points, layer 3 has all route points
            try:
                if len(self.ds[layer_idx]) > 0:
                    return layer_idx
            except IndexError:
                pass
        raise GPXImportError("Could not guess which GPX layer to use.")
    
    def to_linestring(self, layer_idx=None):
        '''
        :returns: the waypoints/track/route as GEOS MultiLineString. Tries
        to automatically detect which layer to use when no layer is provided.
        '''
        if not layer_idx:
            layer_idx = self._guess_layer()
        layer = self.ds[layer_idx]
        if layer_idx == 4 or layer_idx == 3:
            return MultiLineString(LineString(layer.get_geoms(geos=True)))
