'''
module for gpx conversion tasks
'''
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.gis.geos.linestring import LineString
from osgeo import ogr
import os

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
        Returns the waypoints/track/route as GEOS LineString. Tries
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
        for feature_idx in range(lyr.GetFeatureCount()):
            feature = lyr.GetFeature(feature_idx)
            gdal_obj = feature.GetGeometryRef()
            # TODO: should run some profiling to check which conversion
            # format is fastest / most efficient
            geos_obj = GEOSGeometry(buffer(gdal_obj.ExportToWkb()))
            objs.append(geos_obj)
        return objs