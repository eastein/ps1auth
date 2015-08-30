from django import forms
from ldap3 import ALL_ATTRIBUTES, BASE
from accounts.backends import get_ldap_connection, PS1Backend
from member_management.models import Person
from accounts.models import PS1User
from uuid import UUID


class AssociateAccountsForm(forms.Form):
    ldap_dn = forms.CharField(widget=forms.HiddenInput)
    person_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_ldap_dn(self):
        with get_ldap_connection() as c:
            c.search(
                search_base=self.cleaned_data['ldap_dn'],
                search_filter='(objectClass=User)',
                search_scope=BASE,
                attributes=ALL_ATTRIBUTES
            )
        object_guid = c.response[0]['attributes']['objectGUID'][0]
        guid = UUID(bytes_le=object_guid)
        self.user = PS1Backend().get_user(guid)

    def clean_person_id(self):
        person_id = self.cleaned_data['person_id']
        self.person = Person.objects.get(id=person_id)
        if self.person.user is not None:
            raise forms.ValidationError('%{person}s already has a username %{username}s',
                                        params={'person': self.person, 'username': self.person.user})

    def associate(self):
        self.person.user = self.user
        self.person.save()
