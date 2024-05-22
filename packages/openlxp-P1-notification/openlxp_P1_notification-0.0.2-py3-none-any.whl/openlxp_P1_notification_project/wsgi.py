"""
WSGI config for openlxp_P1_notification_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from openlxp_P1_notification.management.utils.p1ps_requests import (
    get_team_templates)

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'openlxp_P1_notification_project.settings')
get_team_templates()


application = get_wsgi_application()
