import uuid
from django.http import HttpResponseRedirect, HttpResponseForbidden

from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from ldap3 import LEVEL, ALL_ATTRIBUTES, BASE

from accounts.backends import get_ldap_connection
from .forms import AssociateAccountsForm
from member_management.models import Person


class LdapUser(object):
    def __init__(self, ldap_record):
        self.dn = ldap_record['dn']
        self.uuid = uuid.UUID(bytes_le=ldap_record['attributes']['objectGuid'][0])
        self.person = Person.objects.filter(user_id=self.uuid).first()


def unmatched_ldap_accounts(request):
    context = {}
    with get_ldap_connection() as c:
        c.search(
            search_base=settings.AD_BASEDN,
            search_filter='(objectClass=User)',
            search_scope=LEVEL,
            attributes=ALL_ATTRIBUTES
        )
        context['ldap_users'] = filter(lambda ldap_user: ldap_user.person is None,
                                       map(lambda user: LdapUser(user), c.response))

    return render(request, 'audit/ldap.html', context)


def ldap_account(request, ldap_dn):
    context = {}
    with get_ldap_connection() as c:
        c.search(
            search_base=ldap_dn,
            search_filter='(objectClass=User)',
            search_scope=BASE,
            attributes=ALL_ATTRIBUTES
        )
        context['ldap_user'] = LdapUser(c.response[0])
        context['entry'] = c.entries[0]
        context['ldif'] = c.entries[0].entry_to_ldif
        context['people'] = map(
            lambda person: (person, AssociateAccountsForm(initial={'ldap_dn': ldap_dn, 'person_id': person.id})),
            Person.objects.filter(user__isnull=True))

    return render(request, 'audit/ldap_user.html', context)


def link_ldap_account_to_mm_entry(request):
    if request.method == 'POST':
        form = AssociateAccountsForm(request.POST)
        if form.is_valid():
            form.associate()
            messages.success(request, 'Successfully Link LDAP Account with Member Management entry.')
        else:
            messages.error(request, 'There was an error linking the LDAP Account with the Member Management entry.')
        return HttpResponseRedirect(reverse('audit.views.unmatched_ldap_accounts'))
    else:
        return HttpResponseForbidden()
