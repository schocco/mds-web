'''
module for gpx conversion tasks
:deprecated: in favour of load2.py
'''
import os

from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos.error import GEOSException
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.gis.geos.linestring import LineString
from django.contrib.gis.gdal import DataSource
from osgeo import ogr

import logging
logger = logging.getLogger(__name__)

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
        self.ds = ogr.Open(self.gpx_file)
        # Unset the environment variable, so it doesn't affect other
        # GPX DataSource objects.
        if(dim3):
            os.environ.pop('GPX_ELE_AS_25D')
        
        if self.ds is None:
            raise GPXImportError("Cant use %s as datasource" % file_path)
    
    def _guess_layer(self):
        '''
        Guess which layer contains the relevant trail data.
        It is most likely that the route or track layer contains the complete trail.
        If those are not present, it is checked whether there are enough waypoints
        that could make a complete trail.
        '''
        for lay in (2, 1, 0): # track, route, waypoints
            if self.ds.GetLayer(lay).GetFeatureCount() > 0:
                return lay
        raise GPXImportError("Could not guess which GPX layer to use.")
    
    def to_linestring(self, layer=None):
        '''
        Returns the waypoints/track/route as GEOS MultiLineString. Tries
        to automatically detect which layer to use when no layer is provided.
        
        The following types are not handled:
        - polygon (typeid 3)
        - multipoint (typeid 4)
        - multipolygon (typeid 6)
        '''
        if not layer:
            layer = self._guess_layer()
        geom = self.get_layer_geometry(layer)
        if(geom is None or len(geom) == 0):
            return None
        elif(len(geom) == 1):
            geom = geom[0]
            if(geom.geom_typeid == 5): # MultiLineString
                return geom # pylint: disable=E1103
            if(geom.geom_typeid == 1): # LineString
                return MultiLineString(geom)
        else:
            return MultiLineString(LineString(geom))
            
    def _get_layer(self, layer):
        '''
        Get OGR layer by id.
        '''
        if layer > self.ds.GetLayerCount():
            raise IndexError('Layer index is out of range')
        return self.ds.GetLayer(layer)
    
    def get_layer_geometry(self, layer=0):
        '''
        Generic method to return any geometry object of the gpx file as GEOSGeometry obj.
        By default uses layer 0.
        
        Returns an empty list when layer is empty or not present.
        '''       
        lyr = self._get_layer(layer)
        objs = []
        print "Number of layers is %d" % lyr.GetFeatureCount() 
        for feature_idx in range(lyr.GetFeatureCount()):
            feature = lyr.GetFeature(feature_idx)
            gdal_obj = feature.GetGeometryRef()
            print gdal_obj.__class__.__name__
            print "Geometryname is %s" % str(gdal_obj.geom_name)
            geos_obj = None
            # TODO: should run some profiling to check which conversion
            # format is fastest / most efficient
            try:
                gdal_obj.IsValid()
                buf = buffer(gdal_obj.ExportToWkb())
                geos_obj = GEOSGeometry(buf)
                objs.append(geos_obj)
            except RuntimeError, e:
                # this can happen, when a geometrycollection is invalid,
                # e.g. when a LineString only has a single point but needs at least 2
                # try to iterate over all children to fix this problem
                
                print e
        return objs