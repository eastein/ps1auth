from django.conf.urls import patterns, include, url
import accounts.views
import accounts.forms
#import django.contrib.auth.views.password_reset_done

urlpatterns = patterns('',
    url(r'login/$', 'django.contrib.auth.views.login', {}),
    url(r'logout/$', 'django.contrib.auth.views.logout', {}),
    url(r'password_change/$', 'django.contrib.auth.views.password_change', {}),
    url(r'password_change_done/$', 'django.contrib.auth.views.password_change_done', {}),
    url(r'password_reset/$', 'django.contrib.auth.views.password_reset',
        {
            'password_reset_form': accounts.forms.PasswordResetForm,
            'post_reset_redirect': 'django.contrib.auth.views.password_reset_done',
        }, name='password-reset'),
    url(r'password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {}),
    #url(r'password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 'django.contrib.auth.views.password_reset_confirm', {}),
    #url(r'password_reset_confirm/(?P<uidb36>[0-9A-Za-z\-]+)/(?P<token>[0-9A-Za-z\-]+)$', 'django.contrib.auth.views.password_reset_confirm', {}),
    url(r'password_reset_confirm/(?P<uid>[0-9A-Za-z\-]+)/(?P<token>[0-9A-Za-z\-]+)$', 'accounts.views.password_reset_confirm', {}),
    url(r'password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', {}),
    url(r'set_password/$', 'accounts.views.set_password', {}),
    url(r'edit_groups/(?P<user_id>.+)', 'accounts.views.edit_groups_for_user'),
#    url(r'access/$', 'accounts.views.access_page', {}),
#    url(r'audits/$', 'accounts.views.audits', {}),
)
