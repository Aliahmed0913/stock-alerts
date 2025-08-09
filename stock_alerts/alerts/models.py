from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.core.validators import MinValueValidator
# Create your models here.
User = get_user_model()

class Alert(models.Model):
    
    class alertsTypes(models.TextChoices):
        THRESHOLD = 'threshold','THRESHOLD'
        DURATION = 'duration','DURATION'
    
    compare_symbols = [
        ('>', 'greaterThan'),
        ('<', 'lessThan'),
        ('=', 'equal'),
    ]
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    stock_symbol = models.CharField(max_length = 50)   
    alert_type = models.CharField(max_length = 10, 
                                  choices = alertsTypes.choices)
    
    comparison = models.CharField(max_length = 1, choices = compare_symbols)  
    target_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    duration = models.DurationField(default=timedelta(minutes = 5))
    is_active = models.BooleanField(default=True)
    has_triggered = models.BooleanField(default=False)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    
class TriggeredAlert(models.Model):
     
    class TriggeredMethods(models.TextChoices):
        THRESHOLD = 'threshold','THRESHOLD'
        DURATION = 'duration','DURATION'
        
    alert = models.ForeignKey(Alert, on_delete = models.CASCADE)
    trigger_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    triggered_at = models.DateTimeField(auto_now_add = True)
    triggered_method = models.CharField(max_length = 10, choices = TriggeredMethods.choices)
    
    def __str__(self):
        return f'{self.alert.stock_symbol} triggered at {self.triggered_at}'