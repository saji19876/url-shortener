from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^account/', include('django_authopenid.urls')),
    (r'^$', 'shortener.views.index'),    
    (r'^admin/(.*)', admin.site.root),    
    (r'^submit/$', 'shortener.views.submit'),
    (r'^(?P<base62_id>\w+)$', 'shortener.views.follow'),
    (r'^info/(?P<base62_id>\w+)$', 'shortener.views.info'),   
    (r'^(?P<stat_type>v)/(?P<base62_id>\w+)$', 'shortener.views.follow'),
    (r'^(?P<user_id>\d+)/(?P<username>\w+)$', 'shortener.views.user'),
    
    # API
    (r'^api/v1/shorten$', 'shortener.views.shorten'),
    (r'^api/v1/expand$', 'shortener.views.shorten'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_DOC_ROOT}),
)
