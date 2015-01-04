# -*- coding: utf-8 -*-

from django.conf.urls import url
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import NotFound
from tastypie.resources import Resource, ModelResource
from tastypie.validation import CleanedDataFormValidation

from apps.mds_auth.authorization import ReadAllSessionAuthentication, \
    ReadAllDjangoAuthorization
from apps.muni_scales.fields import MscaleFieldMixin
from apps.muni_scales.forms import UDHscaleForm, UXCscaleForm
from apps.muni_scales.models import UDHscale, UXCscale
from apps.muni_scales.mscale import Mscale, MSCALES


class MscaleField(fields.ApiField, MscaleFieldMixin):
    '''
    A field that accepts an Mscale Resource but stores the integer value in the db.
    '''
    dehydrated_type = 'apps.muni_scales.mscale.Mscale'
    help_text = 'an mscale object'
    
    def convert(self, value):
        if value is None:
            return None
        return self.to_mscale(value)
    
    def hydrate(self, bundle):
        '''
        Prepare data before saving to the model.
        '''
        #check if value present
        if bundle.data.has_key(self.instance_name):
            value = bundle.data[self.instance_name]
            mscale = self.to_mscale(value)
            return mscale.number
        else:
            return None
    
    def dehydrate(self, bundle, **kwargs):
        '''
        Prepare data for serialization before sending to the client.
        '''
        return self.convert(1)

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
            url(r"^(?P<resource_name>%s)/(?P<pk>[0-9]+)/$" %
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
        try:
            pk = float(kwargs['pk'])
            return MSCALES[pk]
        except KeyError:
            raise NotFound("Invalid lookup ID provided.")
        except ValueError:
            raise NotFound()



class ScaleCalcMixin(object):
    '''
    Adds endpoint for score calculation.
    '''
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/calculate/$" % 
                self._meta.resource_name, self.wrap_view('get_score'), name="calc_udh_score"),
        ]
        
    def get_score(self, request, **kwargs):
        '''
        Return the score for the calculation
        '''
        scale = self.__class__()
        bundle = scale.build_bundle(data=request.POST, request=request)
        scale_obj = scale.full_hydrate(bundle).obj
        errors = scale_obj.full_clean()
        if errors:
            return self.create_response(request, errors)
        score = scale_obj.get_score()
        return self.create_response(request, score)


class UDHResource(ScaleCalcMixin, ModelResource):
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
    maximum_difficulty = MscaleField(attribute="maximum_difficulty")#fields.ToOneField(MscaleResource, attribute="maximum_difficulty")
    average_difficulty = MscaleField(attribute="average_difficulty")#fields.ToOneField(MscaleResource, attribute="average_difficulty")
    score = fields.DictField(attribute='get_score', readonly=True, use_in="detail")
    trail = fields.ToOneField("apps.trails.api.TrailResource", "trail", related_name="udhscale", null=True);

    
    class Meta:
        queryset = UDHscale.objects.all()
        resource_name = 'udh-scale'
        validation = CleanedDataFormValidation(form_class = UDHscaleForm)
        always_return_data = True
        #TODO: proper permission checks
        authentication = ReadAllSessionAuthentication()
        authorization = ReadAllDjangoAuthorization()



class UXCResource(ScaleCalcMixin, ModelResource):
    '''
    UXC Rating
    '''
    maximum_difficulty = MscaleField(attribute="maximum_difficulty")
    average_difficulty = MscaleField(attribute="average_difficulty")
    score = fields.DictField(attribute='get_score', readonly=True, use_in="detail")
    trail = fields.ToOneField("apps.trails.api.TrailResource", "trail", related_name="uxcscale", null=True);
     
    class Meta:
        queryset = UXCscale.objects.all()
        resource_name = 'uxc-scale'
        always_return_data = True
        validation = CleanedDataFormValidation(form_class = UXCscaleForm)
        authentication = ReadAllSessionAuthentication()
        authorization = ReadAllDjangoAuthorization()
