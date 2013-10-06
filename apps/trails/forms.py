'''
Forms used for validation in tastypie api
'''
from apps.trails.models import Trail
from django import forms

class TrailForm(forms.ModelForm):
    class Meta:
        model = Trail