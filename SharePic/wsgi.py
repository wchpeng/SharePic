"""
WSGI config for SharePic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get("PY3_DJANGO2_SETTING_ENV", "develop")
print("-------------------------------")
print(env)
print("-------------------------------")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SharePic.%s' % env)

application = get_wsgi_application()
