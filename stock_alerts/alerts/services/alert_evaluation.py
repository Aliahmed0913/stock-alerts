from alerts.models import Alert
from .triggers import threshold_trigger,duration_trigger 
from .fetch_prices import request_for_prices
import logging

logger = logging.getLogger('alerts')

def active_untriggered_alert_symbols():
    active_alerts = Alert.objects.filter(has_triggered = False, is_active = True)
    alerts_symbols = active_alerts.values_list('stock_symbol', flat = True,).distinct()
    return alerts_symbols    

def evaluate_alerts():
    active_alerts = Alert.objects.filter(has_triggered = False, is_active = True)
    
    if not active_alerts.exists():
            logger.warning('There is no alert to tracking!')
            return
        
    untriggered_symbols = active_untriggered_alert_symbols()
    current_prices = request_for_prices(untriggered_symbols)
        
    for alert in active_alerts:       
        if alert.alert_type == 'threshold':
             threshold_trigger(alert = alert, current_prices = current_prices)
        elif alert.alert_type == 'duration':
              duration_trigger(alert = alert, current_prices = current_prices)
      