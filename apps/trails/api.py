# -*- coding: utf-8 -*-
import tempfile

from django.conf.urls import url
from django.contrib.gis.measure import Distance
from django.http.response import HttpResponse
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.contrib.gis.resources import GeometryApiField
from tastypie.contrib.gis.resources import ModelResource
from tastypie.exceptions import BadRequest
from tastypie.http import HttpNoContent
from tastypie.utils.urls import trailing_slash
from tastypie.validation import CleanedDataFormValidation

from apps.mds_auth.api import UserResource
from apps.mds_auth.authorization import ReadAllDjangoAuthorization, \
    ReadAllSessionAuthentication
from apps.muni_scales.api import UXCResource, UDHResource
from apps.trails.api_authorization import TrailAuthorization
from apps.trails.forms import TrailForm
from apps.trails.load2 import GPXImportError
from apps.trails.models import Trail
from apps.trails.tasks import get_linestring


class DistanceField(fields.DictField):
    '''
    Field to represent Distance objects.
    '''
    help_text = "A dictionary of data, representing the distance in different units"

    def __init__(self, *args, **kwargs):
        '''
        Like DictField constructor, but takes additional keyword argument "units".
        :param units: a list or tuple with units to be included in the object.
                      Supported units are listed at https://docs.djangoproject.com/en/dev/ref/contrib/gis/measure/
        '''
        self.units = kwargs.pop("units", ("m", "km"))
        for unit in self.units:
            if unit not in Distance.UNITS.keys():
                raise Exception("Invalid unit passed into DistanceField: " + str(unit))
        super(DistanceField, self).__init__(*args, **kwargs)
    
    def convert(self, value):
        if value is None:
            return None
        dic = dict()
        for unit in self.units:
            dic[unit] = value.__getattr__(unit)
        return dic

class TrailResource(ModelResource):
    '''
    API resource which includes dynamically calculated values as readonly
    fields. Some fields are only visible in detail view to avoid high computation overhead.
    
    The length attribute is added through the query interface with a call to length().
    '''
    owner = fields.ToOneField(UserResource, 'owner', null=True, blank=True)
    altitude_difference = fields.CharField(attribute='get_altitude_difference', readonly=True)
    length = DistanceField(attribute='length', readonly=True, units=("m", "km", "ft", "mi", "yd"), null=True, blank=True)
    max_slope = fields.CharField(attribute='get_max_slope', readonly=True, use_in="detail")
    max_slope_uh = fields.CharField(attribute='get_max_slope_uh', readonly=True, use_in="detail")
    max_slope_dh = fields.CharField(attribute='get_max_slope_dh', readonly=True, use_in="detail")
    avg_slope = fields.CharField(attribute='get_avg_slope', readonly=True, use_in="detail")
    total_ascent = fields.CharField(attribute='get_total_ascent', readonly=True, use_in="detail")
    total_descent = fields.CharField(attribute='get_total_descent', readonly=True, use_in="detail")
    height_profile = fields.DictField(attribute='get_height_profile', readonly=True, use_in="detail")
    waypoints = GeometryApiField(attribute="waypoints", use_in="detail")
    uxc_rating = fields.ToOneField(UXCResource, 'uxcscale', related_name="trail", null=True, blank=True, full=True)
    udh_rating = fields.ToOneField(UDHResource, 'udhscale', related_name="trail", null=True, blank=True, full=True)

    class Meta:
        queryset = Trail.objects.all().length()
        resource_name = 'trails'
        always_return_data = True
        authentication = ReadAllSessionAuthentication()
        authorization = TrailAuthorization()
        validation = CleanedDataFormValidation(form_class = TrailForm)
        filtering = {
                     'type': ALL,
                     'owner': ALL_WITH_RELATIONS,
                     'created': ALL,
                     'edited': ALL,
                     'name': ALL,
                     }
        ordering = ["name", "length"]

    
    def obj_create(self, bundle, **kwargs):
        'automatically adds the current user to the created model.'
        return super(TrailResource, self).obj_create(bundle, owner=bundle.request.user)

    def prepend_urls(self):
        return [
            # loading GPX files
            url(r"^(?P<resource_name>%s)/load-gpx%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('load_gpx'), name="api_load_gpx"),
            # querying for the geojson result
            url(r"^(?P<resource_name>%s)/load-gpx/result/(?P<task_id>[\w\d-]+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_gpx_result'), name="api_get_geojson")
        ]

    def load_gpx(self, request, **kwargs):
        if request.method == 'POST':
            gpx_file = request.FILES.get('gpx', False)
            ls = None
            if(gpx_file and (gpx_file.name.lower().endswith(".gpx") or gpx_file.name.lower().endswith(".xml")
               and gpx_file.size < 10000)):        
                filehandle, tmpath = tempfile.mkstemp(suffix=".gpx")
                with open(tmpath, 'wb+') as destination:
                    for chunk in gpx_file.chunks():
                        destination.write(chunk)
                #get linestring                
                r = get_linestring.delay(tmpath)
                return self.create_response(request, {"task_id": r.id})
        raise BadRequest("only gpx/xml files smaller than 10,000 bytes are allowed.")
    
    def get_gpx_result(self, request, **kwargs):
        # get task id
        task_id = kwargs.pop("task_id")
        result = get_linestring.AsyncResult(task_id)
        if result.ready():
            try:
                response = result.get(propagate=True)
                # do not use create_response here, the linestring
                # is already serialized to geojson
                return HttpResponse(response)
            except GPXImportError, e:
                raise BadRequest("File could not be loaded: " + e.message)
        else:
            return self.create_response(request, {}, HttpNoContent)
        
        
    
