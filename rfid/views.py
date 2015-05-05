from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import Resource, RFIDAccessLogEvent, RFIDNumber, WebUnlock, LogEvent
from .forms import KeyForm



def check(request, resource_name, tag_number):
    try:
        tag = RFIDNumber.objects.get(ASCII_125khz=tag_number)
        resource = Resource.objects.get(name=resource_name)
    except (RFIDNumber.DoesNotExist, Resource.DoesNotExist):
        return HttpResponse(content="No", status=404, reason="Resource or Tag not Found")
    if resource.is_allowed(tag):
        log_event = RFIDAccessLogEvent(
            resource = resource,
            user = tag.user,
            rfid_number=tag,
            original_key=tag_number,
        )
        log_event.save()
        return HttpResponse(content="Yes", status=200, reason="Access Allowed")
    else:
        return HttpResponse(content="No", status=403, reason="Access Denied")

@login_required()
def configure_rfid(request):
    try:
        tag = request.user.rfidnumber
    except RFIDNumber.DoesNotExist:
        tag = RFIDNumber(user=request.user)
    if request.method == 'POST':
        form = KeyForm(request.POST, instance=tag)
        if form.is_valid():
            foo = form.save(commit=False)
            foo.save()
            messages.success(request, "RFID tag number updated")
    else:
        request.user.rfidnumber
        form = KeyForm(instance=tag)

    context = {}
    context['form'] = form
    context['title'] = 'Configure RFID'
    return render(request, "ps1auth/form.html", context)

@login_required()
def history(request):
    twelve_hours_ago = timezone.now() + timedelta(hours=-12)
    context = {}
    context['webunlocks'] = WebUnlock.objects.all()
    context['log_events'] = LogEvent.objects.select_subclasses().filter(
        created_on__gte=twelve_hours_ago,
    ).order_by('-created_on')[:30]
    return render(request, "rfid/history.html", context)

@login_required()
def unlock(request, resource_name):
    context = {}
    resource = Resource.objects.get(name=resource_name)
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    resource.webunlock.unlock(request.user, ip_address)
    return JsonResponse(context)
