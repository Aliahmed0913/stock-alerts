from alerts.models import Alert,TriggeredAlert
from users.models import User,UserNotificationSetting
from django.core.cache import cache
from django.utils import timezone
from datetime import datetime

def alerts_should_mail():

    pending_alerts = TriggeredAlert.objects.filter(notification_status = TriggeredAlert.NotificationStatus.PENDING).select_related('alert__user')
    
    users = {pending_alert.alert.user_id for pending_alert in pending_alerts}
    notification_settings = {
    s.user_id: s
    for s in UserNotificationSetting.objects.filter(user_id__in=users, enable_email=True)
    }
    
    if pending_alerts:
        alerts_to_email = []
        for t_alert in pending_alerts:
            current_user_notification = notification_settings[t_alert.alert.user_id]
            last_notification = current_user_notification.last_notified 
            
            if not last_notification:
                alerts_to_email.append((t_alert.alert.user, t_alert.alert, t_alert.trigger_price))
            else:
                time_from_last_cooldown = timezone.now() - last_notification       
                if current_user_notification.cooldown_period <= time_from_last_cooldown:
                    alerts_to_email.append((t_alert.alert.user, t_alert.alert, t_alert.trigger_price))

            
            t_alert.attempts_num += 1
            t_alert.notification_status = TriggeredAlert.NotificationStatus.FAIL
            t_alert.save(update_fields=['attempts_num','notification_status'])
            
        return alerts_to_email
    return
    

def store_success_mail(user,alert):
    notification_settings = UserNotificationSetting.objects.get(user = user)
    triggeredAlert = TriggeredAlert.objects.get(alert = alert, alert__user = user)
   
    notification_settings.last_notified = timezone.now()
    triggeredAlert.notification_status = triggeredAlert.NotificationStatus.SENT
    triggeredAlert.notification_attempt_at = notification_settings.last_notified
    triggeredAlert.attempts_num += 1
   
    triggeredAlert.save(update_fields=['notification_status', 'notification_attempt_at', 'attempts_num'])
    notification_settings.save(update_fields=['last_notified'])