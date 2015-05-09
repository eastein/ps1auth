from django.test import TestCase
from .models import PS1User, PS1Group
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
