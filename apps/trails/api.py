# -*- coding: utf-8 -*-

from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.validation import CleanedDataFormValidation

from apps.muni_scales.api import UXCResource, UDHResource
from apps.trails.forms import TrailForm
from apps.trails.models import Trail
from tastypie.contrib.gis.resources import ModelResource


class TrailResource(ModelResource):
    '''
    API resource which includes dynamically calculated values as readonly
    fields. Fields are only visible in detail view to avoid high computation overhead.
    '''
    altitude_difference = fields.CharField(attribute='get_altitude_difference', readonly=True)
    length = fields.CharField(attribute='get_length', readonly=True)
    max_slope = fields.CharField(attribute='get_max_slope', readonly=True, use_in="detail")
    avg_slope = fields.CharField(attribute='get_avg_slope', readonly=True, use_in="detail")
    total_ascent = fields.CharField(attribute='get_total_ascent', readonly=True, use_in="detail")
    total_descent = fields.CharField(attribute='get_total_descent', readonly=True, use_in="detail")
    height_profile = fields.DictField(attribute='get_height_profile', readonly=True, use_in="detail")
    uxc_rating = fields.ToOneField(UXCResource, 'uxcscale', related_name="trail", null=True, blank=True, full=True)
    udh_rating = fields.ToOneField(UDHResource, 'udhscale', related_name="trail", null=True, blank=True, full=True)
        
    class Meta:
        queryset = Trail.objects.all()
        resource_name = 'trails'
        #TODO: proper permission checks
        authentication = Authentication()
        authorization = Authorization()
        validation = CleanedDataFormValidation(form_class = TrailForm)
