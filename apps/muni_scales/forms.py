'''
Forms used for validation in tastypie api
'''
from apps.muni_scales.models import UDHscale, UXCscale
from django import forms

class UDHscaleForm(forms.ModelForm):
    class Meta:
        model = UDHscale
        # FIXME: temporary workaround until a proper validation solution is found
        # for uri / pk conversion
        exclude = ['average_difficulty', 'maximum_difficulty']
        
class UXCscaleForm(forms.ModelForm):
    class Meta:
        model = UXCscale
        # FIXME: temporary workaround until a proper validation solution is found
        # for uri / pk conversion
        exclude = ['average_difficulty', 'maximum_difficulty']