from django.conf.urls import patterns, url

urlpatterns = patterns('discourse.views',
    url(r'^sso$', 'sso', {}),
)
