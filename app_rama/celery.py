import os
from celery import Celery
from django.conf import settings

#ustawienie domyslnych modulow ustawien Django dla programu celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_rama.settings')

app = Celery('app_rama') #@@@ opcjonalnie mozna tu zmienic app_rame na app

app.config_from_object('django.conf:settings') #@@@opcjonalnie mozna tu przekazac name space
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
