import os
import sys

PROJECT_ROOT, APACHE_DIR = os.path.split(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Enable source code reloading with mod_wsgi
import monitor
monitor.start(interval=1.0)
