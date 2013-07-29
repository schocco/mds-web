# -*- coding: utf-8 -*-
from apps.muni_scales.mscale import Mscale, MSCALES
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource

class MscaleResource(Resource):
    '''
    A read-only Mscale resource.
    '''
    id = fields.CharField(attribute='id')
    underground = fields.CharField(attribute='underground')
    slope = fields.CharField(attribute='slope')
    obstacles = fields.ListField(attribute='obstacles')
    characteristics = fields.ListField(attribute='characteristics')

    class Meta:
        resource_name = 'mscale'
        object_class = Mscale
        authorization = Authorization()
        
    # The following methods will need overriding regardless of your
    # data source.
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):
        return MSCALES

    def obj_get_list(self, request=None, **kwargs):
        # TODO: proper filtering
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        #TODO: get obj
        return None

    def obj_delete(self, request=None, **kwargs):
        raise Exception("not allowed.")

    def rollback(self, bundles):
        pass
