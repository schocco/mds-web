import json
import os
import time

from django.contrib.auth.models import User
from django.contrib.gis.geos import MultiLineString, LineString
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from apps.trails.load2 import GPXReader
from models import Trail

# time to wait between retrying api calls
WAIT_INTERVAL = 0.05

class ManualTrailConstructionTest(TestCase):
    '''
    Creates linestrings manually and assigns them to trails.
    '''
    fixtures = ["users.json"]
    
    
    def test_creation(self):
        t1 = Trail()
        t1.name = "Testtrail1"
        t1.owner = User.objects.get(pk=1)
        t1.waypoints = MultiLineString(LineString((48.75118072, 8.539638519, 712),
                                  (48.75176078, 8.541011810, 696),
                                  (48.75133635, 8.545153141, 556),
                                  (48.75067140, 8.545582294, 531)))
        t1.save()
        self.assertIsNotNone(t1.created, 'timestamp has not been added automatically')
        self.assertIsNotNone(t1.edited, 'timestamp has not been added automatically')
        t1.name="Testtrail"
        t1.save()
        self.assertGreater(t1.edited, t1.created, 'edited timestamp was not updated after save operation')
        
    
class ImportGPXTest(TestCase):
    '''
    Test layermapping from gpx to linestrings for trail creation.
    '''
    fixtures = ["users.json"]
    
    def test_import(self):
        '''
        Uses the load module to read gpx data, which contains long, lat and altitude
        '''
        path = os.path.dirname( __file__ )
        gpx_file = os.path.join(path, 'data/BadWildbad.gpx')
        self.assertTrue(os.path.exists(gpx_file))
        ls = GPXReader(gpx_file)
        self.assertIsNotNone(ls.to_linestring())
        
        t1 = Trail()
        t1.name = "Testtrail GPX"
        t1.owner = User.objects.get(pk=1)
        t1.waypoints = ls.to_linestring()
        t1.save()
        self.assertIsNotNone(t1.created, 'timestamp has not been added automatically')
        self.assertIsNotNone(t1.edited, 'timestamp has not been added automatically')
        
        
        
    def test_gpx_upload(self):
        '''Uploading GPX files should succeed'''
        response = self._upload_file('data/BadWildbad.gpx')
        self.assertEqual(response.status_code, 200)
        response = self._upload_file('data/oruxmaps-unicon17-xc.gpx')
        self.assertEqual(response.status_code, 200)
        task_id = json.loads(response.content).get("task_id")
        response = self._get_geojson(task_id, 0.5)
        jsonObj = json.loads(response.content)
        # the resulting json is a multilinestring where each point
        # has 3 dimensions (lat,lon,ele)
        point = jsonObj['coordinates'][0][0]
        self.assertEqual(len(point), 3, "Points must include elevation data")
        
    def test_invalid_upload(self):
        'Uploading other files should fail'
        response1 = self._upload_file('api.py')
        self.assertEqual(response1.status_code, 400, 'wrong file types should be detected immediately')
        response2 = self._upload_file('data/empty.gpx')
        self.assertEqual(response2.status_code, 200)

        c = Client()
        tid2 = json.loads(response2.content).get("task_id")
        response2b = self._get_geojson(tid2, 0.2)
        self.assertEqual(response2b.status_code, 400)
   
   
    def _upload_file(self, file_path):
        'Uploads a file and returns the response object.'
        c = Client()
        path = os.path.dirname( __file__ )
        gpx_file = os.path.join(path, file_path)
        self.assertTrue(os.path.exists(gpx_file))
        with open(gpx_file) as fp:
            response = c.post(reverse('api_load_gpx', kwargs={'resource_name':'trails', 'api_name':'v1'}), {'gpx': fp})
        return response
    
    def _get_geojson(self, task_id, max_wait=1):
        '''
        Calls the api method to get the result for the executed gpx load task.
        Retry on empty results until max_wait time is exceeded.
        '''
        total_wait = 0
        c = Client()
        while True:
            resp = c.get(reverse('api_get_geojson',
                                 kwargs={'resource_name':'trails', 'api_name':'v1', 'task_id':task_id}))
            if(total_wait > max_wait):
                self.fail("Maximum wait time exceeded for api call.")                                      
            if(resp.status_code == 204):
                time.sleep(WAIT_INTERVAL)
                total_wait += WAIT_INTERVAL
            else:
                break
        return resp
            
            
class TrailFunctionTest(TestCase):
    '''
    Tests functions / properties of trail objects.
    '''
    fixtures = ["users.json"]
    
    def setUp(self):
        ls2d = MultiLineString(LineString((48.75118072, 8.539638519, 0),
                          (48.75176078, 8.541011810, 0),
                          (48.75133635, 8.545153141, 0),
                          (48.75067140, 8.545582294, 0)))
        ls3d = MultiLineString(LineString((48.75118072, 8.539638519, 540),
                          (48.75176078, 8.541011810, 696),
                          (48.75133635, 8.545153141, 556),
                          (48.75067140, 8.545582294, 531)))
        owner = User.objects.get(pk=1)
        Trail.objects.create(name="3d waypoints", waypoints = ls3d, owner=owner)
        Trail.objects.create(name="2d waypoints", waypoints = ls2d, owner=owner)
        
    def test_altitude_functions(self):
        '''
        Checks correct altitude calculations.
        '''
        d3 = Trail.objects.get(name="3d waypoints")
        d2 = Trail.objects.get(name="2d waypoints")
        # altitude sections
        self.assertEquals(len(d2._get_altitude_sections()), 3)
        self.assertEqual(len(d3._get_altitude_sections()), 3)
        # total altitude uphill
        self.assertEqual(d3.get_total_ascent(), 696 - 540)
        self.assertEqual(d2.get_total_ascent(), 0)
        # total altitude downhill        
        self.assertEqual(d3.get_total_descent(), 696 - 531)
        self.assertEqual(d2.get_total_descent(), 0)
        
    def test_length_functions(self):
        '''
        tests length calculations
        '''
        d3 = Trail.objects.get(name="3d waypoints")
        d2 = Trail.objects.get(name="2d waypoints")
        
        self.assertEqual(d3._get_length_sections(), d2._get_length_sections())
        
        self.assertGreater(d3.trail_length, d2.trail_length, "Altitude data should be taken into account when calculating length")
        self.assertGreater(d2.trail_length, 0)
        
    def test_slope_functions(self):
        '''
        tests slope calculations
        '''
        d3 = Trail.objects.get(name="3d waypoints")
        
        self.assertEqual(len(d3._get_slope_sections()), 3)
        # slope may be higher than 140% in general, but in this case it shouldn't be
        max_slope = abs(d3.get_max_slope())
        self.assertTrue(max_slope > 0 and max_slope <= 140)
        self.assertLess(d3.get_max_slope(dh=True), 0)
        self.assertGreater(d3.get_max_slope(uh=True), 0)
        # the steepest part is the first uphill section
        self.assertEqual(d3.get_max_slope(), d3.get_max_slope(uh=True))
        self.assertTrue(abs(d3.get_avg_slope()) > 0 and d3.get_avg_slope() <= d3.get_max_slope(), 'avg slope must not be higher than maximum slope')
