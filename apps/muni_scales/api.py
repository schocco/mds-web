# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http.response import HttpResponse
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import ImmediateHttpResponse, BadRequest
from tastypie.http import HttpBadRequest
from tastypie.resources import Resource, ModelResource
from tastypie.utils.mime import build_content_type
from tastypie.validation import CleanedDataFormValidation

from apps.muni_scales.forms import UDHscaleForm, UXCscaleForm
from apps.muni_scales.models import UDHscale, UXCscale
from apps.muni_scales.mscale import Mscale, MSCALES
from apps.trails.models import Trail


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
        
    def apply_sorting(self, obj_list, options=None):
        """
        sorts by number (always ascending)
        """
        return sorted(obj_list, key=lambda m: m.number)

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
   # trail = fields.ToOneField("apps.trails.api.TrailResource", "trail", related_name="udhscale", null=True);
    
    
    class Meta:
        queryset = UDHscale.objects.all()
        resource_name = 'udh-scale'
        validation = CleanedDataFormValidation(form_class = UDHscaleForm)
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/calculate/$" % 
                self._meta.resource_name, self.wrap_view('get_score'), name="calc_udh_score"),
        ]
        
    def get_score(self, request, **kwargs):
        '''
        Return the score for the calculation
        '''
        scale = UDHResource()
        bundle = scale.build_bundle(data=request.POST, request=request)
        udh = scale.full_hydrate(bundle).obj
        errors = udh.full_clean()
        if errors:
            return self.create_response(request, errors)
        score = udh.get_score()
        return self.create_response(request, score)
    
class UXCResource(ModelResource):
    '''
    UXC Rating
    '''
    maximum_difficulty = fields.ToOneField(MscaleResource, attribute="maximum_difficulty")
    average_difficulty = fields.ToOneField(MscaleResource, attribute="average_difficulty")
    score = fields.DictField(attribute='get_score', readonly=True, use_in="detail")
   # trail = fields.ToOneField("apps.trails.api.TrailResource", "trail", related_name="uxcscale", null=True);
     
    class Meta:
        queryset = UXCscale.objects.all()
        resource_name = 'uxc-scale'
        validation = CleanedDataFormValidation(form_class = UXCscaleForm)
    
    #FIXME: duplicate code, refactor!
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/calculate/$" % 
                self._meta.resource_name, self.wrap_view('get_score'), name="calc_uxc_score"),
        ]
    
    def get_score(self, request, **kwargs):
        '''
        Return the score for the calculation
        '''
        scale = UXCResource()
        bundle = scale.build_bundle(data=request.POST, request=request)
        form = UXCscaleForm(request.POST)
        if form.is_valid():
            uxc = scale.full_hydrate(bundle).obj
            score = uxc.get_score()
            return self.create_response(request, score)
        else:
            if request:
                desired_format = self.determine_format(request)
            else:
                desired_format = self._meta.default_format
            errors = form.errors
            serialized = self.serialize(request, errors, desired_format)
            response = HttpBadRequest(content=serialized, content_type=build_content_type(desired_format))
            raise ImmediateHttpResponse(response=response)
