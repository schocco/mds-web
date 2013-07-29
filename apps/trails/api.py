# -*- coding: utf-8 -*-

from apps.trails.models import Trail
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource



class TrailResource(ModelResource):
    gpx = fields.FileField()
    
    class Meta:
        queryset = Trail.objects.all()
        resource_name = 'trails'
        #TODO: proper permission checks
        authentication = Authentication()
        authorization = Authorization()
     
    def hydrate(self, bundle):
        #TODO: extract info from GPX and put points in linestring field "waypoints"
        return bundle