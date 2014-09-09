from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from tastypie.api import Api

from apps.auth.api import SocialSignUpResource, BackendResource, UserResource
from apps.muni_scales.api import MscaleResource, UDHResource, UXCResource
from apps.trails.api import TrailResource


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MscaleResource())
v1_api.register(TrailResource())
v1_api.register(UDHResource())
v1_api.register(UXCResource())
v1_api.register(SocialSignUpResource())
v1_api.register(BackendResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name = 'index'),
    url(r'^go-to-django/$', RedirectView.as_view(url='http://djangoproject.com'), name='go-to-django'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    # authentication stuff
#    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
#    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
#    url(r'^accounts/pw-change/$', 'django.contrib.auth.views.password_change'),
#    url(r'^accounts/pw-change-done/$', 'django.contrib.auth.views.password_change_done'),
#    url(r'^accounts/pw-reset-done/$', 'django.contrib.auth.views.password_reset_done'),
#    url(r'^accounts/pw-reset/$', 'django.contrib.auth.views.password_reset'),
#    url(r'^accounts/pw-reset-confirm/$', 'django.contrib.auth.views.password_reset_confirm'),
#    url(r'^accounts/pw-reset-complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url('', include('social.apps.django_app.urls', namespace='social')),
#   url(r'^auth/social', TemplateView.as_view(template_name='social_auth.html')),
)