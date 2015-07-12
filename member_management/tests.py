from accounts.models import PS1User
from .models import (
    IDCheck,
    Person,
)
from django.core.urlresolvers import reverse
from django.db import transaction
from django.test import Client, TestCase
import reversion


class PersonTest(TestCase):

    def setUp(self):
        self.user = PS1User.objects.create_superuser("testuser", password="Garbage1",  email="foo@bar.com")
        self.client = Client()
        result = self.client.login(username='testuser', password='Garbage1')
        self.assertTrue(result)

    def tearDown(self):
        PS1User.objects.delete_user(self.user)

    def test_page_without_user(self):
        person = Person(
            first_name = "no_user",
            last_name = "none"
        )
        person.save()
        url = '/mm/person/{}'.format(person.pk)
        response = self.client.get(url)

        self.assertEquals(200, response.status_code)

    def test_page_with_user_and_no_groups(self):
        lonely_person = Person(
            first_name = "lonely",
            last_name = "person"
        )
        lonely_person.save()
        lonely = PS1User.objects.create_user("lonely", password="Garbage1",  email="lonely@example.com")
        self.assertIsNotNone(lonely_person)
        lonely_person.user = lonely
        lonely_person.save()

        # view a person with a user account and no groups
        url = '/mm/person/{}'.format(lonely_person.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        #cleanup
        PS1User.objects.delete_user(lonely)

    def test_pending_count(self):
        p1 = Person.objects.create(first_name=".", last_name=".", membership_status="starving_hacker")
        Person.objects.create(first_name="1", last_name=".", membership_status="full_member")

        # Two new members should show up pending, since they have no ID checks
        self.assertEqual(2, Person.objects.pending_members().count())

        # One member got an ID checked once, and should still show up as pending
        IDCheck.objects.create(person=p1, user=self.user)
        self.assertEqual(2, Person.objects.pending_members().count())

        # With another ID check, that member should not show up as pending
        IDCheck.objects.create(person=p1, user=self.user)
        self.assertEqual(1, Person.objects.pending_members().count())

    def test_person_admin_history(self):
        with transaction.atomic(), reversion.create_revision():
            person =  Person(
                first_name = "lonely",
                last_name = "person"
            )
            person.save()

        first_version = reversion.get_for_object(person)[0]
        url = reverse('admin:member_management_person_revision', args=(person.id,first_version.id))
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

class QuorumTest(TestCase):

    def test_no_members(self):
        self.assertEqual(1, Person.objects.quorum())

    def test_no_full_members(self):
        Person.objects.create(first_name=".", last_name=".", membership_status="starving_hacker")
        self.assertEqual(1, Person.objects.quorum())

    def test_quorum(self):
        # no members
        self.assertEqual(1, Person.objects.quorum())

        Person.objects.create(first_name="1", last_name=".", membership_status="full_member")
        self.assertEqual(1, Person.objects.quorum())

        Person.objects.create(first_name="2", last_name=".", membership_status="full_member")
        self.assertEqual(1, Person.objects.quorum())

        Person.objects.create(first_name="3", last_name=".", membership_status="full_member")
        self.assertEqual(1, Person.objects.quorum())

        Person.objects.create(first_name="4", last_name=".", membership_status="full_member")
        self.assertEqual(2, Person.objects.quorum())
