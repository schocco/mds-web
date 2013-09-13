# -*- coding: utf-8 -*-
from apps.muni_scales.fields import MscaleField
from apps.muni_scales.models import UDHscale, UXCscale
from apps.muni_scales.mscale import Mscale, MSCALES
from django.conf.urls import url
from django.utils import simplejson
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.fields import ApiField, CharField
from tastypie.resources import Resource, ModelResource

class MscaleResource(Resource):
    '''
    A read-only Mscale resource.
    '''
    id = fields.DecimalField(attribute='number')
    underground = fields.CharField(attribute='underground')
    slope = fields.CharField(attribute='slope')
    obstacles = fields.ListField(attribute='obstacles')
    characteristics = fields.ListField(attribute='characteristics')

    class Meta:
        resource_name = 'mscales'
        object_class = Mscale
        authorization = Authorization()
        allowed_methods = ['get']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/$" %
                    self._meta.resource_name,
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.number
        else:
            kwargs['pk'] = bundle_or_obj.number
        return kwargs

    def get_object_list(self, request):
        return MSCALES.values()

    def obj_get_list(self, request=None, **kwargs):
        # TODO: proper filtering
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        pk = float(kwargs['pk'])
        return MSCALES[pk]

class UDHResource(ModelResource):
    '''
    UDH rating
    
from apps.muni_scales.api import *
from apps.muni_scales.models import UDHscale
data={'maximum_difficulty':2,'average_difficulty':1, 'total_length':12, 'average_slope':20}

scale = UDHResource()
udh = UDHscale(**data)
bundle = scale.build_bundle(udh)
scale.full_dehydrate(bundle)
    '''
    maximum_difficulty = fields.ToOneField(MscaleResource, attribute="maximum_difficulty")
    average_difficulty = fields.ToOneField(MscaleResource, attribute="average_difficulty")
    score = fields.DictField(attribute='get_score', readonly=True, use_in="detail")
    
    
    class Meta:
        queryset = UDHscale.objects.all()
        resource_name = 'udh-scale'
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/calculate/$" % 
                self._meta.resource_name, self.wrap_view('get_score'), name="api_dispatch_detail"),
        ]
        
    def get_score(self, request, **kwargs):
        '''
        Return the score for the calculation
        '''
        scale = UDHResource()
        #TODO: check input data
        scale_bundle = scale.build_bundle(data=request.POST, request=request)
        return self.create_response(request, scale_bundle)
    
class UXCResource(ModelResource):
    '''
    UXC Rating
    '''
    maximum_difficulty = fields.ToOneField(MscaleResource, attribute="maximum_difficulty")
    average_difficulty = fields.ToOneField(MscaleResource, attribute="average_difficulty")
    
    class Meta:
        queryset = UXCscale.objects.all()
        resource_name = 'uxc-scale'    