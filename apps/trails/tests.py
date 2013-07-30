"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from apps.trails.load import GPXMapping
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
        track_mapping = {'waypoints' : 'LINESTRING'}
        lm = GPXMapping(Trail, gpx_file, track_mapping, layer=1)
        lm.model.name = "test track"
        self.assertIsNotNone(lm.model.waypoints)
        
        t1 = Trail()
        t1.name = "Testtrail GPX"
        t1.waypoints = lm.get_values()['waypoints']
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