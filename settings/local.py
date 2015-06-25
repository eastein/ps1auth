from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1:8001', '127.0.0.1']


MERCHANT_SETTINGS = {
    'pay_pal': {
        'RECEIVER_EMAIL': 'money@pumpingstationone.org',
    }
}
PAYPAL_RECEIVER_EMAIL = MERCHANT_SETTINGS['pay_pal']['RECEIVER_EMAIL']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(SITE_ROOT, 'cache'),
    }
}

INSTALLED_APPS += (
#    "debug_toolbar",
    "django_jenkins",
)

INTERNAL_IPS = (
    "127.0.0.1",
    "10.0.2.2",
)

MIDDLEWARE_CLASSES = (
#    "debug_toolbar.middleware.DebugToolbarMiddleware",
) + MIDDLEWARE_CLASSES

MEDIA_ROOT = os.path.join(SITE_ROOT,'media')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(SITE_ROOT, 'cache', 'mail')
