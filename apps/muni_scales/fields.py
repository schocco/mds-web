from decimal import Decimal

from django import forms
from django.db.models.fields import DecimalField
from django.db.models.fields.subclassing import SubfieldBase
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _

from mscale import MSCALE_CHOICES, Mscale, MSCALES


class MscaleFormField(forms.fields.DecimalField):

    '''
    Form field for the mscale type.
    '''

    def __init__(self, max_value=None, min_value=None, max_digits=None, 
                 decimal_places=None, *args, **kwargs):
        widget = Select(choices=MSCALE_CHOICES)
        super(MscaleFormField, self).__init__(*args, widget=widget, **kwargs)


class MscaleFieldMixin(object):

    '''
    Mixin for the conversion to mscale objects
    from other representation forms.
    '''

    def to_mscale(self, value):
        ''':returns: value as an Mscale object'''
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if isinstance(value, Mscale) or value is None:
            return value
        if isinstance(value, (str, unicode)):
            value = unicode(value.upper().strip("M"))
            value = float(value)
        if isinstance(value, (float, int, Decimal)):
            value = float(value)
        else:
            raise ValueError("Got unexpected format %r" % value)
        return MSCALES.get(value)


class MscaleField(DecimalField, MscaleFieldMixin):

    ''''
    M scale, describing the difficultiy of a single muni trail section.
    '''
    # If  null=True i sallowed, any field method that takes value as
    # an argument, like to_python() and get_prep_value(), should handle the
    # case when value is None.
    description = _(
        "M scale, describing the difficultiy of a single muni trail section.")
    __metaclass__ = SubfieldBase

    def __init__(self, *args, **kwargs):
        '''Creates DecimalField with fixed number of digits and decimal places.'''
        kwargs['max_digits'] = 2
        kwargs['decimal_places'] = 1
        super(MscaleField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        ''':returns: value as an Mscale object'''
        return self.to_mscale(value)

    def get_db_prep_save(self, value, connection):
        '''
        prepare value for storage in the db.
        '''
        if value is None:
            return None
        return connection.ops.value_to_db_decimal(self.get_prep_value(value),
                                                  self.max_digits, self.decimal_places)

    def get_prep_value(self, value):
        '''
        opposite of to_python, should receive an Mscale object.
        '''
        number = self.to_python(value).number  # pylint: disable=E1103
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
