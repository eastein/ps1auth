from django.conf.urls import patterns, include, url

urlpatterns = patterns('rfid.views',
    url(r'configure/$', 'configure_rfid'),
    url(r'check/(?P<resource_name>\w+)/(?P<tag_number>[0-9a-fA-F]{12})$', 'check'),
    url(r'history', 'history'),
    url(r'unlock/(?P<resource_name>\w+)', 'unlock')
)
