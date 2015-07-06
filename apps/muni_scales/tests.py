from models import UDHscale, UXCscale
from django.test import TestCase


class CaclulationTestCase(TestCase):

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
