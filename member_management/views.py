from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .forms import PersonForm, IDCheckForm, PayPalForm, PersonSearchForm
from .models import Person, EmailTemplate, EmailRecord, IDCheck
from .tables import PersonTable
from math import ceil
import reversion
from django_tables2 import RequestConfig

@staff_member_required
def send_templated_email(request, email_template_id, person_id=None):
    email_template = EmailTemplate.objects.get(pk = email_template_id)
    if person_id:
        recipient = Person.objects.get(pk=person_id)
    else:
        recipient = None
    count = email_template.send(request.user, recipient)
    if count == 1:
        messages.success(request, 'Sent "{}" to "{}'.format(email_template, recipient))
    elif count == 0:
        messages.error(request, 'Failed to Send "{}" to "{}'.format(email_template, recipient))
    else:
        messages.info(request, "sending {} to {} recipients".format(email_template, count))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@staff_member_required
def send_test_templated_email(request, email_template_id):
    return send_templated_email(request, email_template_id, person_id=request.user.person.pk)

@login_required()
def member_list(request):
    data = {}
    data['full_members'] = Person.objects.full_members().order_by('last_name')
    data['starving_hackers'] = Person.objects.starving_hackers().order_by('last_name')
    data['member_count'] = Person.objects.members().count()
    data['quorum_count'] = Person.objects.quorum()
    return render(request, 'member_management/member_list.html', data)

@staff_member_required
def person_detail(request, person_id=None):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        person = None
    if person and hasattr(person, 'paypal'):
        paypal = person.paypal
    else:
        paypal = None

    if request.method == 'POST':
        person_form = PersonForm(request.POST, prefix='person', instance=person)
        paypal_form = PayPalForm(request.POST, prefix='paypal', instance=paypal)
        # avoid short circuit evaluation
        person_form_is_valid = person_form.is_valid()
        paypal_form_is_valid = person_form.is_valid()
        if person_form_is_valid and paypal_form_is_valid:
            with transaction.atomic(), reversion.create_revision():
                person = person_form.save()
                paypal = paypal_form.save(commit=False)
                paypal.person = person
                paypal.save()
                reversion.set_user(request.user)
                messages.success(request, 'Saved Changes Successfully')
                if '_save_and_check_id' in request.POST:
                    return HttpResponseRedirect(reverse(id_check, kwargs={'person_id': person.pk}))
                elif '_save_and_send_email' in request.POST:
                    email_template_id = request.POST['_save_and_send_email']
                    email_template = EmailTemplate.objects.get(id=email_template_id)
                    count = email_template.send(request.user, person)
                    if count == 1:
                        messages.success(request, 'Sent "{}" to "{}'.format(email_template, person))
                    elif count == 0:
                        messages.error(request, 'Failed to Send "{}" to "{}'.format(email_template, person))
                    return HttpResponseRedirect(person.get_absolute_url())
                else:
                    return HttpResponseRedirect(person.get_absolute_url())
    else:
        person_form = PersonForm(prefix='person', instance=person)
        paypal_form = PayPalForm(prefix='paypal', instance=paypal)
    data = {}
    data['person_form'] = person_form
    data['paypal_form'] = paypal_form
    data['email_records'] = EmailRecord.objects.filter(recipient=person)
    data['person'] = person
    data['id_checks'] = IDCheck.objects.filter(person=person)
    data['email_templates'] = EmailTemplate.objects.individual_recipient()
    return render(request, 'member_management/detail.html', data)

@staff_member_required
def person_list(request): 
    # poor mans search
    search_form = PersonSearchForm(request.GET)

    if search_form.is_valid():
        queryset = search_form.get_queryset()
    else:
        queryset = Person.objects.all()
    data = {}
    table = PersonTable(queryset, order_by="-updated_on")
    RequestConfig(request, paginate={'per_page':100}).configure(table)
    data['table'] = table
    data['search_form'] = search_form
    return render(request, 'member_management/person_list.html', data)

@staff_member_required
def id_check(request, person_id):
    person = Person.objects.get(pk=person_id)
    if request.method == 'POST':
        id_check_form = IDCheckForm(request.POST, person=person)
        id_check_form.full_clean()
        if id_check_form.is_valid():
            id_check = IDCheck(person=person, user=request.user)
            id_check.save()
            return HttpResponseRedirect(person.get_absolute_url())
    else:
        id_check_form = IDCheckForm(person=person)
    data = {}
    data['person'] = person
    data['form'] = id_check_form
    return render(request, 'member_management/id_check.html', data)
