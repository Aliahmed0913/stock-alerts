from celery import shared_task
from alerts.services.alert_evaluation import evaluate_alerts
from notifications.tasks import publish_alert_emails_task
import logging

logger = logging.getLogger('alerts')

@shared_task
def run_evaluation_alert():   
    try:
        logger.info('Start scheduled alert evaluation...')
        evaluate_alerts()
        logger.info('Evaluation completed')
        publish_alert_emails_task.delay()
   
    except Exception as e:
        logger.exception('Evaluation failed:%s',str(e))
        raise
    