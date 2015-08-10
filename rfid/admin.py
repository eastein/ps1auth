from django.contrib import admin
from .models import AdGroupResource, Resource, RFIDNumber, WebUnlock

admin.site.register(Resource)
admin.site.register(RFIDNumber)
admin.site.register(AdGroupResource)
admin.site.register(WebUnlock)
