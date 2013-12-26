'''
Forms used for validation in tastypie api
'''
from apps.trails.models import Trail
from django import forms

class TrailForm(forms.ModelForm):
    '''
    Trail form used to clean data prior to passing them to tastypie.
    '''
    #TODO: introduce geojson field type
    waypoints = forms.CharField(max_length=20000)
    
    class Meta:
        model = Trail