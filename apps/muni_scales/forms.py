'''
Forms used for validation in tastypie api
'''
from apps.muni_scales.models import UDHscale, UXCscale
from django import forms

class UDHscaleForm(forms.ModelForm):
    class Meta:
        model = UDHscale
        
class UXCscaleForm(forms.ModelForm):
    class Meta:
        model = UXCscale