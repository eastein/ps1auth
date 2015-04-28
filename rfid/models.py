from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
import urllib.request


class Resource(models.Model):
    name = models.CharField(max_length=160)

    def is_allowed(self, tag):
        """
        The default implementation just returns if the user is valid or not
        """

        try:
            rfid = RFIDNumber.objects.get(pk=tag.pk)
            return rfid.user.is_active
        except RFIDNumber.DoesNotExist:
            return False

    def __str__(self):
        return self.name

class AdGroupResource(Resource):
    """
    Resource that matches against AD groups.
    """
    ad_group = models.CharField(max_length=255)

    def is_allowed(self, tag):
        try:
            return tag.user.is_active() and self.ad_group in self.ldap_user['memberOf']
        except KeyError:
            return False

class WebUnlock(models.Model):
    resource = models.OneToOneField('Resource')
    url = models.URLField()

    def __str__(self):
        return "{} Unlock".format(self.resource.name)

    def unlock(self):
        return urllib.request.urlopen(self.url)


class RFIDNumber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    ASCII_125khz = models.CharField(default = "", max_length=12, unique=True, verbose_name="RFID")

    def __str__(self):
        return u'user={}, RFID={}'.format(self.user, self.ASCII_125khz)

class LogEvent(models.Model):
    models.ForeignKey('Resource')
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

class RFIDAccessLogEvent(LogEvent):
    pass

class ButtonPressLogEvent(LogEvent):
    pass
