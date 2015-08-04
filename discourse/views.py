import base64
import hmac
import hashlib
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings

from urllib import parse, request, error

@login_required
def sso(request):
    payload = request.GET.get('sso')
    signature = request.GET.get('sig')
    support_email=format(settings.SUPPORT_EMAIL_ADDRESS)

    if None in [payload, signature]:
        return HttpResponseBadRequest('No SSO payload or signature. Please {} support if this problem persists.'.format(support_email))

    ## Validate the payload

    try:
        payload = bytes(parse.unquote(payload), 'utf-8')
        decoded = base64.decodestring(payload)
        assert b'nonce' in decoded
        assert len(payload) > 0
    except AssertionError:
        return HttpResponseBadRequest('Invalid payload. Please contact {} if this problem persists.'.format(support_email))

    key = bytes(settings.DISCOURSE_SSO_SECRET, 'utf-8') # must be unicode for python3
    h = hmac.new(key, payload, digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        return HttpResponseBadRequest('Invalid payload. Please contact {} if this problem persists.'.format(support_email))

    ## Build the return payload

    qs = parse.parse_qs(decoded)
    params = {
        'nonce': qs[b'nonce'][0],
        'email': request.user.email,
        'external_id': request.user.get_username(),
        'username': request.user.get_short_name(),
    }

    return_payload = base64.encodestring(bytes(parse.urlencode(params), 'utf-8'))
    h = hmac.new(key, return_payload, digestmod=hashlib.sha256)
    query_string = parse.urlencode({'sso': return_payload, 'sig': h.hexdigest()})

    ## Redirect back to Discourse

    url = '%s/session/sso_login' % settings.DISCOURSE_BASE_URL
    return HttpResponseRedirect('%s?%s' % (url, query_string))
