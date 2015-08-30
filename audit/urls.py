from django.conf.urls import patterns, url

urlpatterns = patterns('audit.views',
                       url(r'^unmatched_ldap_accounts$', 'unmatched_ldap_accounts', {}),
                       url(r'^ldap_account/(?P<ldap_dn>.+)$', 'ldap_account', {}),
                       url(r'^link_accounts$', 'link_ldap_account_to_mm_entry', {})
                       )
