from django.db.models.fields import DecimalField
from django.forms.fields import Field
from django.utils.translation import ugettext_lazy as _
from mscale import Mscale, MSCALES

class MscaleFormField(Field):
    '''
    Form field for the mscale type.
    '''

class MscaleField(DecimalField):
    ''''
    M scale, describing the difficultiy of a single muni trail section.
    '''
    #If  null=True i sallowed, any field method that takes value as
    # an argument, like to_python() and get_prep_value(), should handle the case when value is None.
    description = _("M scale, describing the difficultiy of a single muni trail section.")

    def __init__(self, *args, **kwargs):
        '''Creates DecimalField with fixed number of digits and decimal places.'''
        kwargs['max_digits'] = 2
        kwargs['decimal_places'] = 1
        super(MscaleField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        ''':returns: value as an Mscale object'''
        if isinstance(value, Mscale) or value is None:
            return value
        if isinstance(value, str):
            str.upper().strip("M")
            value = float(value)
        if isinstance(value, float) or isinstance(value, int):
            value = float(value)
        return MSCALES.get(value)
            
    
    def get_prep_value(self, value):
        '''
        given the db entry, return a mscale object.
        '''
        return self.to_python(value).number # pylint: disable=E1103

        
    def formfield(self, **kwargs):
        '''
        Returns the appropriate formfield.
        '''
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': MscaleFormField}
        defaults.update(kwargs)
        return super(MscaleField, self).formfield(**defaults)