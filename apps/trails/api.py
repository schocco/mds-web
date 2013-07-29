# -*- coding: utf-8 -*-

from apps.trails.models import Trail
from tastypie.resources import ModelResource



class TrailResource(ModelResource):
    class Meta:
        queryset = Trail.objects.all()
        resource_name = 'trails'