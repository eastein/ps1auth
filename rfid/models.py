from django.db import models
from django.conf import settings
import logging
from model_utils.managers import InheritanceManager
import urllib.request
from accounts.models import PS1Group

logger = logging.getLogger(__name__)


class Resource(models.Model):
    name = models.CharField(max_length=160)
    display_name = models.CharField(max_length=160)

    def is_allowed(self, tag):
        """
        The default implementation just returns if the user is valid or not
        """
        return tag.user.is_active

    def __str__(self):
        return self.display_name

class AdGroupResource(Resource):
    """
    Resource that matches against AD groups.
    """
    group = models.ForeignKey(PS1Group)

    def is_allowed(self, tag):
        return tag.user.is_active() and self.group.has_user(tag.user)

class WebUnlock(models.Model):
    resource = models.OneToOneField('Resource')
    url = models.URLField()

    def __str__(self):
        return "{} Unlock".format(self.resource.name)

    def unlock(self, user, ip_address):
        event = ButtonPressLogEvent(
            resource = self.resource,
            user = user,
            ip_address = ip_address,
        )
        logger.info(ip_address)
        event.save()
        result = urllib.request.urlopen(self.url)
        return result

class RFIDNumber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    ASCII_125khz = models.CharField(default = "", max_length=12, unique=True, verbose_name="RFID")

    def __str__(self):
        return u'user={}, RFID={}'.format(self.user, self.ASCII_125khz)

class LogEvent(models.Model):
    resource = models.ForeignKey('Resource')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(auto_now_add=True, blank=False)
    objects = InheritanceManager()

class RFIDAccessLogEvent(LogEvent):
    rfid_number = models.ForeignKey('RFIDNumber', blank=False)
    original_key = models.CharField(max_length=12, blank=False)

class ButtonPressLogEvent(LogEvent):
    ip_address = models.GenericIPAddressField(blank=False)

    def __str__(self):
        return "ButtonPressLogEvent(resource={},user={},created_on={},ip_address={})".format(
            self.resource,
            self.user,
            self.created_on,
            self.ip_address,
        )
