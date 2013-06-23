from django import forms
from django.db.models.fields import DecimalField
from django.db.models.fields.subclassing import SubfieldBase
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _
from mscale import MSCALE_CHOICES, Mscale, MSCALES
from south.modelsinspector import add_introspection_rules

class MscaleFormField(forms.fields.DecimalField):
    '''
    Form field for the mscale type.
    '''
    def __init__(self, max_value=None, min_value=None, max_digits=None, decimal_places=None, *args, **kwargs):
        widget = Select(choices = MSCALE_CHOICES)
        super(MscaleFormField, self).__init__(*args, widget=widget, **kwargs)

class MscaleField(DecimalField):
    ''''
    M scale, describing the difficultiy of a single muni trail section.
    '''
    #If  null=True i sallowed, any field method that takes value as
    # an argument, like to_python() and get_prep_value(), should handle the case when value is None.
    description = _("M scale, describing the difficultiy of a single muni trail section.")
    __metaclass__ = SubfieldBase
    
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
    
    def get_db_prep_save(self, value, connection):
        '''
        prepare value for storage in the db.
        '''
        return connection.ops.value_to_db_decimal(self.get_prep_value(value),
                self.max_digits, self.decimal_places)
            
    
    def get_prep_value(self, value):
        '''
        opposite of to_python.
        '''
        number = self.to_python(value).number # pylint: disable=E1103
        return number 

        
    def formfield(self, **kwargs):
        '''
        Returns the appropriate formfield.
        '''
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': MscaleFormField}
        defaults.update(kwargs)
        return super(MscaleField, self).formfield(**defaults)
    
# allow using this field with south
add_introspection_rules([], ["^apps\.muni_scales\.fields\.MscaleField"])