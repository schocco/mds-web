# -*- coding: utf-8 -*-

from apps.trails.models import Trail
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.contrib.gis.resources import ModelResource

class TrailResource(ModelResource):
    altitude_difference = fields.CharField(attribute='get_altitude_difference', readonly=True)
    max_slope = fields.CharField(attribute='get_max_slope', readonly=True)
    avg_slope = fields.CharField(attribute='get_avg_slope', readonly=True)
    length = fields.CharField(attribute='get_length', readonly=True)
    total_ascent = fields.CharField(attribute='get_total_ascent', readonly=True)
    total_descent = fields.CharField(attribute='get_total_descent', readonly=True)
        
    class Meta:
        queryset = Trail.objects.all()
        resource_name = 'trails'
        #TODO: proper permission checks
        authentication = Authentication()
        authorization = Authorization()
