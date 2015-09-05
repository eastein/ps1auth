from django.conf.urls import patterns, url, include




urlpatterns = patterns('member_management.views',
    url(r'^send_templated_email/(?P<email_template_id>\d+)/(?P<person_id>\d+)$', 'send_templated_email', {}),
    url(r'^send_templated_email/(?P<email_template_id>\d+)$', 'send_templated_email', {}),
    url(r'^test_email/(?P<email_template_id>\d+)$', 'send_test_templated_email', {}),
    url(r'^member_list/$', 'member_list', {}),
    url(r'^person/(?P<person_id>\d+)$', 'person_detail', {}),
    url(r'^person/$', 'person_detail', {'person_id':None}, name="member_management-add_person"),
    url(r'^people/$', 'person_list'),
    url(r'^id_check/(?P<person_id>\d+)$', 'id_check'),
)
