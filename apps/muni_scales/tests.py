import json
from django.contrib.auth.models import User
from django.contrib.gis.geos import LineString, MultiLineString
from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCase
from apps.mds_auth.tests import SessionAuthMixin
from apps.muni_scales.fields import MscaleFieldMixin
from apps.muni_scales.forms import UDHscaleForm, UXCscaleForm
from apps.trails.models import Trail
from models import UDHscale, UXCscale
from django.test import TestCase


class ApiTestCase(ResourceTestCase, SessionAuthMixin):
    '''
    Tests creation and removal of scale objects via the API.
    '''
    def setUp(self):
        super(ApiTestCase, self).setUp()

        # Create a user.
        self.username = 'user'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'user@example.com', self.password)

        # create a trail
        self.t1 = Trail(name = "Testtrail1", owner = self.user)
        self.t1.waypoints = MultiLineString(LineString((48.75118072, 8.539638519, 712),
                                  (48.75176078, 8.541011810, 696),
                                  (48.75133635, 8.545153141, 556),
                                  (48.75067140, 8.545582294, 531)))
        self.t1.save()
        self.t1_url = reverse('api_dispatch_detail', kwargs={'resource_name':'trails', 'api_name':'v1', "pk": self.t1.id})
        self.list_url = reverse('api_dispatch_list', kwargs={'resource_name':'udh-scale', 'api_name':'v1'})
        self.post_data = {
            "avg_difficulty": 2,
            "avg_slope": 8,
            "max_difficulty": 3,
            "total_length": 2000,
            "trail": self.t1_url
        }

    def test_unauthenticated_save(self):
        'Unauthenticated users must not create score objects'
        self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data))

    def test_authenticated_save(self):
        """
        Authenticted users should be able to create ratings for their own trails.
        Returned data should match posted data.
        :return:
        """
        self.login(self.username, self.password)
        response = self.api_client.post(self.list_url, format='json', data=self.post_data)
        self.assertHttpCreated(response)
        self.assertValidJSON(response.content)
        scale = json.loads(response.content)
        to_mscale = MscaleFieldMixin().to_mscale
        self.assertEqual(to_mscale(scale["avg_difficulty"]).number, to_mscale(self.post_data["avg_difficulty"]).number)
        self.assertEqual(to_mscale(scale["max_difficulty"]).number, to_mscale(self.post_data["max_difficulty"]).number)
        self.logout()


class ValidationTest(TestCase):
    """
    Make sure scale objects are properly validated
    """
    def setUp(self):
        self.user = User.objects.create_user("username", 'user@example.com', "userpw")
        # create a DH trail
        self.t1 = Trail(name = "Testtrail1", owner = self.user, type="dh")
        self.t1.waypoints = MultiLineString(LineString((48.75118072, 8.539638519, 712),
                                  (48.75176078, 8.541011810, 696),
                                  (48.75133635, 8.545153141, 556),
                                  (48.75067140, 8.545582294, 531)))
        self.t1.save()
        # and an XC trail
        self.t2 = Trail(name = "Testtrail1", owner = self.user, type="xc")
        self.t2.waypoints = MultiLineString(LineString((48.75118072, 8.539638519, 712),
                                  (48.75176078, 8.541011810, 696),
                                  (48.75133635, 8.545153141, 556),
                                  (48.75067140, 8.545582294, 731)))
        self.t2.save()

        self.udh_data = {
            "avg_difficulty": 5,
            "max_difficulty": 3,
            "avg_slope": 10,
            "total_length": 3000,
            "trail": self.t1.pk
        }
        self.uxc_data = {
            "avg_difficulty": 5,
            "max_difficulty": 3,
            "max_slope_uh": 10,
            "total_length": 3000,
            "total_ascent": 500,
            "trail": self.t2.pk
        }

    def test_avg_max_validation(self):
        """
        Makes sure that avg is <= to max difficulty on UDH and UXC scales.
        """
        form = UXCscaleForm(self.uxc_data)
        self.assertFalse(form.is_valid(), "average must not be higher than maximum")
        form = UDHscaleForm(self.udh_data)
        self.assertFalse(form.is_valid(), "average must not be higher than maximum")
        self.udh_data["max_difficulty"] = 5
        form = UDHscaleForm(self.udh_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_missing_field(self):
        self.udh_data.pop("avg_slope")
        form = UDHscaleForm(self.udh_data)
        self.assertFalse(form.is_valid(), "all fields should be mandatory")




class CalculationTestCase(TestCase):
    """
    Tests calculation using example from the official PDF release of the scales.
    """

    def setUp(self):
        UDHscale.objects.create(total_length="6000", max_difficulty=3.5,
                                avg_difficulty=1.5, avg_slope=16)
        UXCscale.objects.create(total_length="42000", max_difficulty=1.5,
                                avg_difficulty=0.5, total_ascent=590, max_slope_uh=8)

    def test_dh_results(self):
        """checks if calculated dh results are as expected."""
        dh = UDHscale.objects.get(total_length="6000")

        dh_result = dh.get_score()

        self.assertEqual(dh_result['total_length']['value'], dh.total_length)
        self.assertEqual(dh_result['total_length']['result'], 9)

        self.assertEqual(dh_result['avg_slope']['value'], dh.avg_slope)
        self.assertEqual(dh_result['avg_slope']['result'], 4.4)

        self.assertEqual(
            dh_result['max_difficulty']['value'], dh.max_difficulty)
        self.assertEqual(dh_result['max_difficulty']['result'], 8)

        self.assertEqual(
            dh_result['avg_difficulty']['value'], dh.avg_difficulty)
        self.assertEqual(dh_result['avg_difficulty']['result'], 4)

        self.assertEqual(
            dh_result['total_score'], 25, "Got an unexpected result for the DH track")

    def test_xc_results(self):
        '''checks if calculated XC results are as expected.'''
        xc = UXCscale.objects.get(total_length="42000")
        xc_result = xc.get_score()

        self.assertEqual(xc_result['total_length']['value'], xc.total_length)
        self.assertEqual(xc_result['total_length']['result'], 15)

        self.assertEqual(xc_result['total_ascent']['value'], xc.total_ascent)
        self.assertEqual(xc_result['total_ascent']['result'], 4.4)

        self.assertEqual(xc_result['max_slope_uh']['value'], xc.max_slope_uh)
        self.assertEqual(xc_result['max_slope_uh']['result'], 0.8)

        self.assertEqual(
            xc_result['max_difficulty']['value'], xc.max_difficulty)
        self.assertEqual(xc_result['max_difficulty']['result'], 2)

        self.assertEqual(
            xc_result['avg_difficulty']['value'], xc.avg_difficulty)
        self.assertEqual(xc_result['avg_difficulty']['result'], 1.5)

        self.assertEqual(
            xc_result['total_score'], 24, "Got an unexpected result for the XC track")
