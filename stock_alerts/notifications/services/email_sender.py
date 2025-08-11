from users.models import User
from alerts.models import Alert

from django.core.mail import EmailMultiAlternatives ,EmailMessage
from stock_alerts.settings import DEFAULT_FROM_EMAIL

from django.template.loader import render_to_string
from .evaluator import alerts_should_mail, store_success_mail
import logging 

logger = logging.getLogger('notifications')




def publish_alerts_emails():
    
    try:
        alerts_detail = alerts_should_mail()
        
        if not alerts_detail:
            logger.warning("No pending alerts to email.")
            return
       
        for user,alert,current_price in alerts_detail:
            
            subject = f'Stock alert {alert.stock_symbol} reached {current_price}'
            from_email = DEFAULT_FROM_EMAIL
            send_to = [user.email]

            html_content = render_to_string('emails/email_struct.html',{'user': user,
                'alert': alert,
                'current_price': current_price})

            email = EmailMessage(subject, html_content, from_email, send_to)
            email.content_subtype = 'html'
            
            email.send()
            store_success_mail(user,alert)
            logger.info(f"Stock alert email sent to {user.email} for {alert.stock_symbol}")
        
    except Exception as e:
        raise

