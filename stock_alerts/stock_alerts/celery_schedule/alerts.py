from celery.schedules import crontab

ALERT_BEAT_SCHEDULE = {
    'evaluate-stock-alerts-every-3-minutes': {
        'task': 'alerts.tasks.run_evaluation_alert', 
        'schedule': crontab(minute='*/3'),  
    },
}