"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from apps.trails.load import GPXReader
from django.contrib.gis.geos import LineString
from django.test import TestCase
from django.test.client import Client
from models import Trail
import os

       
class ManualTrailConstructionTest(TestCase):
    '''
    Creates linestrings manually and assigns them to trails.
    '''
    
    def test_creation(self):
        t1 = Trail()
        t1.name = "Testtrail1"
        t1.save()
        self.assertIsNotNone(t1.created, 'timestamp has not been added automatically')
        self.assertIsNotNone(t1.edited, 'timestamp has not been added automatically')
        t1.waypoints = LineString((48.75118072, 8.539638519, 712),
                                  (48.75176078, 8.541011810, 696),
                                  (48.75133635, 8.545153141, 556),
                                  (48.75067140, 8.545582294, 531))
        t1.save()
        self.assertGreater(t1.edited, t1.created, 'edited timestamp was not updated after save operation')
        
    
class ImportGPXTest(TestCase):
    '''
    Test layermapping from gpx to linestrings for trail creation.
    '''
    
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
        t1.waypoints = ls.to_linestring()
        t1.save()
        self.assertIsNotNone(t1.created, 'timestamp has not been added automatically')
        self.assertIsNotNone(t1.edited, 'timestamp has not been added automatically')
        
    def test_file_upload(self):
        c = Client()
        path = os.path.dirname( __file__ )
        gpx_file = os.path.join(path, 'data/BadWildbad.gpx')
        self.assertTrue(os.path.exists(gpx_file))
        with open(gpx_file) as fp:
            c.post('/load-gpx/', {'gpx': fp})
            
            
class TrailFunctionTest(TestCase):
    '''
    Tests functions / properties of trail objects.
    '''
    def setUp(self):
        ls2d = LineString((48.75118072, 8.539638519, 0),
                          (48.75176078, 8.541011810, 0),
                          (48.75133635, 8.545153141, 0),
                          (48.75067140, 8.545582294, 0))
        ls3d = LineString((48.75118072, 8.539638519, 540),
                          (48.75176078, 8.541011810, 696),
                          (48.75133635, 8.545153141, 556),
                          (48.75067140, 8.545582294, 531))
        Trail.objects.create(name="no waypoints")
        Trail.objects.create(name="3d waypoints", waypoints = ls3d)
        Trail.objects.create(name="2d waypoints", waypoints = ls2d)
        
    def test_altitude_functions(self):
        '''
        Checks correct altitude calculations.
        '''
        no = Trail.objects.get(name="no waypoints")
        d3 = Trail.objects.get(name="3d waypoints")
        d2 = Trail.objects.get(name="2d waypoints")
        # altitude sections
        self.assertEquals(no._get_altitude_sections(), [])
        self.assertEquals(len(d2._get_altitude_sections()), 3)
        self.assertEqual(len(d3._get_altitude_sections()), 3)
        # total altitude uphill
        self.assertEqual(no.get_total_ascent(), 0)
        self.assertEqual(d3.get_total_ascent(), 696 - 540)
        self.assertEqual(d2.get_total_ascent(), 0)
        # total altitude downhill        
        self.assertEqual(no.get_total_descent(), 0)
        self.assertEqual(d3.get_total_descent(), 696 - 531)
        self.assertEqual(d2.get_total_descent(), 0)
        
    def test_length_functions(self):
        '''
        tests length calculations
        '''
        no = Trail.objects.get(name="no waypoints")
        d3 = Trail.objects.get(name="3d waypoints")
        d2 = Trail.objects.get(name="2d waypoints")
        
        self.assertEqual(no._get_length_sections(), [])
        self.assertEqual(d3._get_length_sections(), d2._get_length_sections())
        
        self.assertEqual(no.get_length(), 0)
        self.assertEqual(d3.get_length(), d2.get_length())
        self.assertGreater(d2.get_length(), 0)
        
    def test_slope_functions(self):
        '''
        tests slope calculations
        '''
        no = Trail.objects.get(name="no waypoints")
        d3 = Trail.objects.get(name="3d waypoints")
        d2 = Trail.objects.get(name="2d waypoints")
        
        self.assertEqual(len(d3._get_slope_sections()), 3)
        self.assertEqual(no._get_slope_sections(), [])
        # slope may be higher than 140% in general, but in this case it shouldn't be
        self.assertTrue(d3.get_max_slope() > 0 and d3.get_max_slope() <= 140)
        self.assertGreater(d3.get_max_slope(dh=True), 0)
        self.assertGreater(d3.get_max_slope(uh=True), 0)
        # the steepest part is the first uphill section
        self.assertEqual(d3.get_max_slope(), d3.get_max_slope(uh=True))
        self.assertTrue(abs(d3.get_avg_slope()) > 0 and d3.get_avg_slope() <= d3.get_max_slope(), 'avg slope must not be higher than maximum slope')