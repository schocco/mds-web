from models import UDHscale, UXCscale
from django.test import TestCase


class CaclulationTestCase(TestCase):
    def setUp(self):
        UDHscale.objects.create(total_length="6000", maximum_difficulty=3.5,
                                average_difficulty=1.5, average_slope=16)
        UXCscale.objects.create(total_length="3000", maximum_difficulty=3,
                                average_difficulty=2, total_ascent=300, maximum_slope_uh=20)

    def test_dh_results(self):
        """checks if calculated dh results are as expected."""
        dh = UDHscale.objects.get(total_length="6000")
        
        dh_result = dh.get_score()
        
        self.assertEqual(dh_result.total_length['value'], dh.total_length)
        self.assertEqual(dh_result.total_length['result'], 9)
        
        self.assertEqual(dh_result.avg_slope['value'], dh.average_slope)
        self.assertEqual(dh_result.avg_slope['result'], 4.4)
        
        self.assertEqual(dh_result.max_difficulty['value'], dh.maximum_difficulty)
        self.assertEqual(dh_result.max_difficulty['result'], 8)
        
        self.assertEqual(dh_result.avg_difficulty['value'], dh.average_difficulty)
        self.assertEqual(dh_result.avg_difficulty['result'], 4)
        
        self.assertEqual(dh_result.total_score, 25, "Got an unexpected result for the DH track")
        
    def test_xc_results(self):
        '''checks if calculated XC results are as expected.'''
        xc = UXCscale.objects.get(total_length="3000")
        #TODO: verify results