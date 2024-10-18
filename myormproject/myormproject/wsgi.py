"""
WSGI config for myormproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.save_evento_services import SaveEventoService

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myormproject.settings')

application = get_wsgi_application()

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(SaveEventoService.salvar_evento, 'interval', minutes=60)
    
    scheduler.start()

start_scheduler()