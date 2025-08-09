from celery import Celery
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_alerts.settings')

celery_app = Celery('stock_alerts')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()