# -*- coding: utf-8 -*-

from apps.trails.models import Trail
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.contrib.gis.resources import ModelResource 

class TrailResource(ModelResource):
    
    class Meta:
        queryset = Trail.objects.all()
        resource_name = 'trails'
        #TODO: proper permission checks
        authentication = Authentication()
        authorization = Authorization()