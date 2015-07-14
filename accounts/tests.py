from django.test import TestCase
from .models import PS1User, PS1Group
from .forms import EditUserGroupForm, SetPasswordForm
from ldap3 import Server, Connection, SUBTREE, Tls, MODIFY_REPLACE, BASE, ALL_ATTRIBUTES
from django.conf import settings
from django.test import Client
from pprint import pprint
import uuid

class AccountTest(TestCase):

    def setUp(self):
        pass

    def test_create_user(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        self.assertEqual(user.get_short_name(), 'testuser')
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password('Garbage1'))
        self.assertFalse(user.check_password('wrong_password'))
        self.assertEqual("foo@bar.com", user.ldap_user['mail'][0])
        self.assertFalse(user.is_staff)
        PS1User.objects.delete_user(user)

    def test_create_superuser(self):
        user = PS1User.objects.create_superuser("superuser", email='super@user.com', password='Garbage2')
        self.assertTrue(user.is_staff)
        PS1User.objects.delete_user(user)


    def test_login(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        c = Client()
        result = c.login(username='testuser', password='Garbage1')
        self.assertTrue(result)
        PS1User.objects.delete_user(user)

    def test_wrong_password(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        c = Client()
        result = c.login(username='testuser', password='WrongPassword1')
        self.assertFalse(result)
        PS1User.objects.delete_user(user)

class PasswordTest(TestCase):

    def setUp(self):
        self.user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")

    def tearDown(self):
        PS1User.objects.delete_user(self.user)

    def test_reset_valid_password(self):
        data = {}
        data['new_password1'] = "Garbage2"
        data['new_password2'] = "Garbage2"
        form = SetPasswordForm(self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_reset_valid_password_mismatch(self):
        data = {}
        data['new_password1'] = "Garbage3"
        data['new_password2'] = "Garbage4"
        form = SetPasswordForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_reset_invalid_password(self):
        data = {}
        data['new_password1'] = "invalid"
        data['new_password2'] = "invalid"
        form = SetPasswordForm(self.user, data=data)
        # samba will reject this password
        self.assertFalse(form.is_valid())

class GroupTest(TestCase):

    def setUp(self):
        self.superuser = PS1User.objects.create_superuser("superuser", email='super@user.com', password='Garbage2')
        self.client = Client()
        result = self.client.login(username='superuser', password='Garbage2')
        self.assertTrue(result)

    def tearDown(self):
        PS1User.objects.delete_user(self.superuser)

    def test_add_group_user_with_no_groups(self):
        fake_group = PS1Group(
            dn="CN=fake,CN=Users,DC=vagrant,DC=lan",
            display_name="fake"
        )

        fake_group.save()

        lonely = PS1User.objects.create_user("lonely4", password="Garbage1",  email="lonely@example.com")
        self.assertIsNotNone(lonely)

        url = '/accounts/edit_groups/{}'.format(lonely.pk)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        #cleanup
        PS1User.objects.delete_user(lonely)

class GroupActionsTest(TestCase):

    def setUp(self):
        self.user = PS1User.objects.create_user("grouptestuser", password="Garbage1",  email="foo@bar.com")
        self.group = PS1Group.objects.create_group('testgroup')
        self.client = Client()
        result = self.client.login(username='grouptestuser', password='Garbage1')
        self.assertTrue(result)

    def tearDown(self):
        PS1User.objects.delete_user(self.user)
        PS1Group.objects.delete_group(self.group)

    def test_add_and_remove(self):
        add_form_data = {
            'account_pk': self.user.pk,
            'group_dn': self.group.dn,
            'action': 'add'
        }
        add_form = EditUserGroupForm(add_form_data)
        self.assertTrue(add_form.is_valid())
        self.assertTrue(add_form.apply())

        remove_form_data = {
            'account_pk': self.user.pk,
            'group_dn': self.group.dn,
            'action': 'remove'
        }
        remove_form = EditUserGroupForm(remove_form_data)
        self.assertTrue(remove_form.is_valid())
        self.assertTrue(remove_form.apply())

    def test_add_user_to_group_twice(self):
        """ Make sure we handle double submission of form."""
        add_form_data = {
            'account_pk': self.user.pk,
            'group_dn': self.group.dn,
            'action': 'add'
        }
        add_form = EditUserGroupForm(add_form_data)
        self.assertTrue(add_form.is_valid())
        self.assertTrue(add_form.apply())

        add_form2 = EditUserGroupForm(add_form_data)
        self.assertTrue(add_form2.is_valid())
        self.assertFalse(add_form2.apply())

    def test_remove_user_from_a_group_they_are_not_in(self):
        remove_form_data = {
            'account_pk': self.user.pk,
            'group_dn': self.group.dn,
            'action': 'remove'
        }
        remove_form = EditUserGroupForm(remove_form_data)
        self.assertTrue(remove_form.is_valid())
        self.assertFalse(remove_form.apply())
