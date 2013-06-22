from fields import MscaleField
from django.db import models

        
        
class BaseScale(models.Model):
    '''
    Base class for all discipline specific scales.
    '''
    total_length = models.IntegerField()
    maximum_difficulty = MscaleField()
    average_difficulty = MscaleField()
    
    class Meta:
        abstract = True
    
class UDHscale(BaseScale):
    '''
    Represents the overall difficulty of the downhill trail.
    '''
    average_slope = models.IntegerField()
    
    def __unicode__(self):
        return self.get_score()
    
    def get_score(self):
        '''
        Calculates the score with the given attributes.
        '''
        #TODO: implement
        return 0
    
    class Meta:
        verbose_name = "UDH Scale Entity"
        verbose_name_plural = "UDH Scale Entities"
    
    
class UXCscale(BaseScale):
    '''
    Represents the overall difficulty of the cross country trail.
    '''
    total_ascent = models.IntegerField()
    maximum_slope_uh = models.IntegerField()

    
    def __unicode__(self):
        return ""
    
    class Meta:
        verbose_name = "UXC Scale Entity"
        verbose_name_plural = "UXC Scale Entities"