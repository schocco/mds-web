from apps.muni_scales import calculator
from apps.trails.models import Trail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from fields import MscaleField

        
class BaseScale(models.Model):
    """
    Base class for all discipline specific scales.
    """
    trail = models.OneToOneField(Trail, null=True, blank=True)
    total_length = models.IntegerField(_('total length'), 
                                       help_text = _("Total trail length in meters"))
    max_difficulty = MscaleField(_('maximum difficulty'),
                                     help_text =_("Maximum difficulty on the M-Scale"))
    avg_difficulty = MscaleField(_('average difficulty'),
                                     help_text = _("average difficulty on the M-Scale"))
    
    class Meta:
        abstract = True
    
class UDHscale(BaseScale):
    """
    Represents the overall difficulty of the downhill trail.
    """
    avg_slope = models.IntegerField(_("average slope"), help_text = _("average slope in %"))
    
    def __unicode__(self):
        return u'UDH %sm avg %s' % (self.total_length, self.average_difficulty)
    
    def get_score(self, as_dict = True):
        '''
        Calculates the score with the given attributes.
        :rtype: :py:class:`apps.muni_scales.calculator.UDH`
        '''
        udh = calculator.UDH(self)
        if(as_dict):
            return udh.as_dict()
        return udh
    
    class Meta:
        verbose_name = "UDH Scale Entity"
        verbose_name_plural = "UDH Scale Entities"
    
    
class UXCscale(BaseScale):
    '''
    Represents the overall difficulty of the cross country trail.
    '''
    total_ascent = models.IntegerField(_("total ascent"),
                                       help_text = _("total ascent in meters"))
    max_slope_uh = models.IntegerField(_("maximum slope (uphill)"),
                                           help_text = _("slope in % of the steepest uphill section"))

    
    def __unicode__(self):
        return u'UXC %s' % self.average_difficulty
    
    def get_score(self, as_dict = True):
        '''
        Calculates the score with the given attributes.
        '''
        if(as_dict):
            return calculator.UXC(self).as_dict()
        return calculator.UXC(self)
    
    class Meta:
        verbose_name = "UXC Scale Entity"
        verbose_name_plural = "UXC Scale Entities"