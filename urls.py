from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

def myview(request,base62_id = None):
    return HttpResponsePermanentRedirect(reverse("info", args=[base62_id]))
    
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^account/', include('django_authopenid.urls')),
    (r'^$', 'shortener.views.index'),    
    (r'^admin/(.*)', admin.site.root),    
    (r'^submit/$', 'shortener.views.submit'),
    (r'^(?P<base62_id>[A-z0-9]+)$', 'shortener.views.follow',[],"short_follow"),
    (r'^(?P<base62_id>[A-z0-9]+)\+$', myview),
    (r'^info/(?P<base62_id>\w+)$', 'shortener.views.info',[],"info"),   
    (r'^(?P<stat_type>v)/(?P<base62_id>\w+)$', 'shortener.views.follow'),
    (r'^(?P<user_id>\d+)/(?P<username>\w+)$', 'shortener.views.user',[], 'user_info_none'),
    (r'^(?P<user_id>\d+)/(?P<username>[^/]+)/(?P<timeframe>\w+)$', 'shortener.views.user',[], 'user_info_timetable'),
    
    # API
    (r'^api/v1/shorten$', 'shortener.views.shorten'),
    (r'^api/v1/expand$', 'shortener.views.shorten'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_DOC_ROOT}),
)
