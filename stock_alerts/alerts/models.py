from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.core.validators import MinValueValidator
# Create your models here.
User = get_user_model()

class Alert(models.Model):
    
    class AlertsTypes(models.TextChoices):
        THRESHOLD = 'threshold','THRESHOLD'
        DURATION = 'duration','DURATION'
    
    class CompareSymbols(models.TextChoices): 
        GREATER_THAN = '>', 'greaterThan'
        LESS_THAN = '<', 'lessThan'
        EQUAL = '=', 'equal'
    
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    stock_symbol = models.CharField(max_length = 50)   
    alert_type = models.CharField(max_length = 10, 
                                  choices = AlertsTypes.choices)
    
    comparison = models.CharField(max_length = 1, choices = CompareSymbols.choices)  
    target_price = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0.01)])
    duration = models.DurationField(default=timedelta(minutes = 5))
    is_active = models.BooleanField(default=True)
    has_triggered = models.BooleanField(default=False)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    
class TriggeredAlert(models.Model):
    class TriggeredMethod(models.TextChoices):
        THRESHOLD = 'threshold','THRESHOLD'
        DURATION = 'duration','DURATION'
    
    class NotificationStatus(models.TextChoices):
        PENDING = 'pending','PENDING'
        SENT = 'sent','SENT'
        FAIL = 'fail','FAIL'
        
    alert = models.ForeignKey(Alert, on_delete = models.CASCADE)
    trigger_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    triggered_at = models.DateTimeField(auto_now_add = True)
    triggered_method = models.CharField(max_length = 10, choices = TriggeredMethod.choices)
    notification_status = models.CharField(max_length = 10,
                                           choices = NotificationStatus.choices,
                                           default = NotificationStatus.PENDING)
    notification_attempt_at = models.DateTimeField(null=True, blank=True)
    attempts_num = models.IntegerField(default = 0)
    
    class Meta():
        indexes =[
            models.Index(fields=['notification_status'])
                  ] 
    
    def __str__(self):
        return f'{self.alert.stock_symbol} triggered at {self.triggered_at}'