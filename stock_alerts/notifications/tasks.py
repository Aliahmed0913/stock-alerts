from celery import shared_task
from notifications.services.email_sender import publish_alerts_emails
import logging

logger = logging.getLogger('notifications')

@shared_task
def publish_alert_emails_task():
    """
    Returns mail to specific user email. 
    """
    try:
        logger.info('Start scheduled users mailing...')
        
        publish_alerts_emails()
        
        logger.info('mailing completed')
    
    except Exception as e:
        logger.error(str(e))
        
       