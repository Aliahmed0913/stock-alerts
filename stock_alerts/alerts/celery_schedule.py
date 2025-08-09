from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'evaluate-stock-alerts-every-5-minutes': {
        'task': 'alerts.tasks.run_evaluation_alert', 
        'schedule': crontab(minute='*/5'),  
    },
}