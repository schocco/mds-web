'''
Forms used for validation in tastypie api
'''
import decimal

from django import forms

from apps.muni_scales.models import UDHscale, UXCscale


class ScaleForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ScaleForm, self).clean()
        avg_diff = cleaned_data.get("avg_difficulty")
        max_diff = cleaned_data.get("max_difficulty")

        if max_diff < avg_diff:
            raise forms.ValidationError(
                "Maximum difficulty cannot be smaller than average difficulty"
            )


class UDHscaleForm(ScaleForm):
    class Meta:
        model = UDHscale
        exclude = ['trail'] # TODO: change when https://github.com/django-tastypie/django-tastypie/issues/152 resolved


class UXCscaleForm(ScaleForm):
    class Meta:
        model = UXCscale
        exclude = ['trail'] # https://github.com/django-tastypie/django-tastypie/issues/152