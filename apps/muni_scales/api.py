# -*- coding: utf-8 -*-
from apps.muni_scales.mscale import Mscale, MSCALES
from django.conf.urls import url
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
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
