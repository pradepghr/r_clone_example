"""
WSGI config for r_clone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os,sys,site
from django.core.wsgi import get_wsgi_application

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
WORK_DIRECTORY = os.path.join(CURRENT_DIRECTORY, '..')

#Add the site-packages
site.addsitedir('/home/pradeep/examples/r_clone/env/lib/python3.6/site-packages')
sys.path.append(WORK_DIRECTORY)
sys.path.append(os.path.join(WORK_DIRECTORY, '..'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'r_clone.settings')
os.environ['HTTPS'] = "on"
application = get_wsgi_application()
