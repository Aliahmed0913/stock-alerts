from celery import shared_task
from alerts.services.alert_evaluation import evaluate_alerts
import logging

logger = logging.getLogger(__name__)

@shared_task
def run_evaluation_alert():   
    try:
        logger.info('Start scheduled alert evaluation...')
        evaluate_alerts()
        logger.info('Evaluation successfully completed')
   
    except Exception as e:
        logger.exception('Evaluation failed:%s',str(e))
        raise
    