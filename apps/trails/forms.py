'''
Forms used for validation in tastypie api
'''
from django import forms
from django.contrib.gis.forms import ModelForm
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.core.exceptions import ValidationError

from apps.trails.models import Trail
from django.utils import simplejson
from django.forms.fields import CharField

# method accept the core arguments mentioned above (required, label, initial, widget, help_text).
class GeoJsonFormField(forms.Field):
    
    def __init__(self, *args, **kwargs):
        self.geom_type = kwargs.pop("geom_type")
        super(GeoJsonFormField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        '''
        Converts dict to geos object.
        '''
        geos = GEOSGeometry(simplejson.dumps(value))
        return geos
    
    def clean(self, value):
        """
        Validates the given value and returns its "cleaned" value as an
        appropriate Python object.

        Raises ValidationError for any errors.
        """
        try:
            value = self.to_python(value)
        except Exception, e:
            raise ValidationError("The geojson string is invalid. Please provide correct geojson.")
        self.validate(value) # checks if empty
        if self.geom_type != value.geom_type:
            raise ValidationError("Wrong geometry type")
        return value

class TrailForm(ModelForm):
    '''
    Trail form used to clean data prior to passing them to tastypie.
    '''
    waypoints = GeoJsonFormField(required=True, geom_type="MultiLineString")
    
    class Meta:
        model = Trail
        exclude = ['owner']
