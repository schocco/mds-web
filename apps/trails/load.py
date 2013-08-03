'''
module for gpx conversion tasks
'''
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import ogr
import os



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
        self.layers = {}
        self.ds = ogr.Open(self.gpx_file)
        # Unset the environment variable, so it doesn't affect other
        # GPX DataSource objects.
        if(dim3):
            os.environ.pop('GPX_ELE_AS_25D')
        
        if self.ds is None:
            raise Exception("Cant use %s as datasource" % file_path)
    
    def get_layer(self, layer):
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
        lyr = self.get_layer(layer)
        objs = []
        for feature_idx in range(lyr.GetFeatureCount()):
            feature = lyr.GetFeature(feature_idx)
            gdal_obj = feature.GetGeometryRef()
            # TODO: should run some profiling to check which conversion
            # format is fastest / most efficient
            geos_obj = GEOSGeometry(buffer(gdal_obj.ExportToWkb()))
            objs.append(geos_obj)
        return objs