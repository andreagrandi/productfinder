"""
WSGI config for productfinder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "productfinder.settings")
application = get_wsgi_application()

if os.environ.get('PRODUCTFINDER_USE_WHITENOISE'):
    application = DjangoWhiteNoise(application)
