# -*- coding: utf-8 -*-

from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.validation import CleanedDataFormValidation

from apps.muni_scales.api import UXCResource, UDHResource
from apps.trails.forms import TrailForm
from apps.trails.models import Trail
from tastypie.contrib.gis.resources import ModelResource
from django.contrib.gis.measure import Distance

class DistanceField(fields.DictField):
    '''
    Field to represent Distance objects.
    '''
    help_text = "A dictionary of data, representing the distance in different units"

    def __init__(self, *args, **kwargs):
        '''
        Like ApiField constructor, but takes additional keyword argument "units".
        :param units: a list or tuple with units to be included in the object.
                      Supported units are listed at https://docs.djangoproject.com/en/dev/ref/contrib/gis/measure/
        '''
        self.units = kwargs.pop("units", ("m", "km"))
        for unit in self.units:
            if unit not in Distance.UNITS.keys():
                raise Exception("Invalid unit passed into DistanceField: " + str(unit))
        super(DistanceField, self).__init__(*args, **kwargs)
    
    def convert(self, value):
        if value is None:
            return None
        dic = dict()
        for unit in self.units:
            dic[unit] = value.__getattr__(unit)
        return dic

class TrailResource(ModelResource):
    '''
    API resource which includes dynamically calculated values as readonly
    fields. Fields are only visible in detail view to avoid high computation overhead.
    '''
    altitude_difference = fields.CharField(attribute='get_altitude_difference', readonly=True)
    length = DistanceField(attribute='length', readonly=True, units=("m", "km", "ft", "mi", "yd"), null=True, blank=True)
    max_slope = fields.CharField(attribute='get_max_slope', readonly=True, use_in="detail")
    avg_slope = fields.CharField(attribute='get_avg_slope', readonly=True, use_in="detail")
    total_ascent = fields.CharField(attribute='get_total_ascent', readonly=True, use_in="detail")
    total_descent = fields.CharField(attribute='get_total_descent', readonly=True, use_in="detail")
    height_profile = fields.DictField(attribute='get_height_profile', readonly=True, use_in="detail")
    uxc_rating = fields.ToOneField(UXCResource, 'uxcscale', related_name="trail", null=True, blank=True, full=True)
    udh_rating = fields.ToOneField(UDHResource, 'udhscale', related_name="trail", null=True, blank=True, full=True)

        
    class Meta:
        queryset = Trail.objects.all().length()
        resource_name = 'trails'
        always_return_data = True
        #TODO: proper permission checks
        authentication = Authentication()
        authorization = Authorization()
        validation = CleanedDataFormValidation(form_class = TrailForm)
