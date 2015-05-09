from argparse import ArgumentTypeError
from django.core.management.base import BaseCommand, CommandError
from member_management.models import Person
from accounts.models import PS1User
from getpass import getpass
import re
from ldap3 import LDAPConstraintViolationResult


password_requirements = r"""
Password Complexity Requirements
================================

* Your password must be at least 7 characters long.
* Your password must contain at least 3 of the 5 following complexity categories:
** Uppercase characters
** Lowercase characters
** Numbers
** Non-alphanumeric characters: ~!@#$%^&*_-+=`|\(){}[]:;"'<>,.?/
** Any unicode character that is alphabetic but not uppercase or lowercase (glyphs)
* Your password must not contain your username or full name.
"""

def username(username):
    if not re.match(r"^[a-z][a-z0-9]{2,30}$", username):
        error_string = """
        Username must be all lower case,
        start with a letter,
        contain only letters and numbers,
        and be between 3 and 30 characters"""
        raise(ArgumentTypeError(error_string))

    users = PS1User.objects.get_users_by_field('sAMAccountName', username)
    if len(users) > 0:
        error_string = "The username {0} already exists.".format(username)
        raise ArgumentTypeError(error_string)

    return username


class Command(BaseCommand):
    help = "Create a person."
    def add_arguments(self, parser):
        parser.add_argument('username', type=username)
        parser.add_argument('-n', '--name')
        parser.add_argument('-m', '--email')
        parser.add_argument('-p', '--password')


    def handle(self, *args, **options):
        if options['name'] and ' ' in options['name']:
            first_name, last_name = options['name'].split(' ')
        elif options['name']:
            first_name = options['name']
            last_name = ""
        else:
            first_name = options['username']
            last_name = ""

        if options['password']:
            password = options['password']
        else:
            password = getpass()

        person = Person(
            first_name=first_name,
            last_name=last_name,
            email=options['email'],
        )
        person.save()
        user = PS1User.objects.create_superuser(
            options['username'],
            email=options['email'],
            first_name = first_name,
            last_name = last_name,
        )

        self.set_password(user, password)

        person.user = user
        person.save()

    def set_password(self, user, password):
        """ Attempts to set the password, if the password set fails, it tries
        again.
        """
        try:
            user.set_password(password)
        except LDAPConstraintViolationResult as e:
            print(password_requirements)
            shorter_message = e.message.split(':')[-1].strip().capitalize()
            print('The exact reason your password was rejected: "{}"'.format(shorter_message))
            self.set_password(user, getpass())
