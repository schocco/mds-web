from apps.muni_scales.api import MscaleResource, UDHResource, UXCResource
from apps.trails.api import TrailResource
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from tastypie.api import Api

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MscaleResource())
v1_api.register(TrailResource())
v1_api.register(UDHResource())
v1_api.register(UXCResource())

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name = 'index'),
    url(r'^go-to-django/$', RedirectView.as_view(url='http://djangoproject.com'), name='go-to-django'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^load-gpx/', 'apps.trails.views.load_gpx'),
)