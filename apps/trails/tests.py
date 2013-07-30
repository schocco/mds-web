"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.gis.geos import LineString
from models import Trail

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
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
    