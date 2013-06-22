from fields import MscaleField
from django.db import models
from django.utils.translation import ugettext_lazy as _
        
        
class BaseScale(models.Model):
    '''
    Base class for all discipline specific scales.
    '''
    total_length = models.IntegerField(_('total length'), 
                                       help_text = _("Total trail length in meters"))
    maximum_difficulty = MscaleField(_('maximum difficulty'), 
                                     help_text =_("Maximum difficulty on the M-Scale"))
    average_difficulty = MscaleField(_('average difficulty'),
                                     help_text = _("average difficulty on the M-Scale"))
    
    class Meta:
        abstract = True
    
class UDHscale(BaseScale):
    '''
    Represents the overall difficulty of the downhill trail.
    '''
    average_slope = models.IntegerField(_("average slope"), help_text = _("average slope in %"))
    
    def __unicode__(self):
        return u'UDH %s' % self.get_score()
    
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
    total_ascent = models.IntegerField(_("total ascent"),
                                       help_text = _("total ascent in meters"))
    maximum_slope_uh = models.IntegerField(_("maximum slope (uphill)"), 
                                           help_text = _("slope in % of the steepest uphill section"))

    
    def __unicode__(self):
        return u'UXC %s' % self.get_score()
    
    def get_score(self):
        '''
        Calculates the score with the given attributes.
        '''
        #TODO: implement
        return 0
    
    class Meta:
        verbose_name = "UXC Scale Entity"
        verbose_name_plural = "UXC Scale Entities"