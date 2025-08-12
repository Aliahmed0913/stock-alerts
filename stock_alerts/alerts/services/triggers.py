from alerts.models import Alert, TriggeredAlert
from django.utils import timezone 
from django.core.cache import cache
from datetime import datetime

import logging
logger = logging.getLogger('alerts')

def threshold_trigger(alert:Alert, current_prices):
    current_price = stock_current_price(alert.stock_symbol, current_prices)
    
    if check_conditions(alert,current_price):
        trigger_alert(alert, current_price)
        return True  
   
    return False

def duration_trigger(alert:Alert, current_prices):
    current_price = stock_current_price(alert.stock_symbol, current_prices)
    cach_key = f'duration_start_time:{alert.id}'
    
    if check_conditions(alert,current_price):
        cached_start_time = cache.get(cach_key)
        
        if not cached_start_time:
            cache.set(cach_key, timezone.now().isoformat(),timeout = None)
            logger.warning('%s alert not met yet for {%s:%s}',alert.alert_type,alert.stock_symbol,alert.id)
            return False
        else:
            duration_start_time = datetime.fromisoformat(cached_start_time)
            duration_from_start = timezone.now() - duration_start_time
            
            if duration_from_start >= alert.duration:
                trigger_alert(alert, current_price)
                cache.delete(cach_key)
                return True
            
    cache.delete(cach_key)
    return False    


def stock_current_price(stock_symbol,current_prices):
    """
    Return Stock price from list of prices
    """
    try:
        return current_prices[stock_symbol]
   
    except KeyError:
        logger.error('%s price not founded in fetched prices',stock_symbol)
        return None
  
def trigger_alert(alert:Alert, current_price):
    """
    Responsible of triggering alerts by add them to triggeredAlert table 
    """
    alert.has_triggered = True
    alert.is_active = False
    alert.triggered_at = timezone.now()
    alert.save(update_fields=['has_triggered','triggered_at','is_active'])
    
    TriggeredAlert.objects.create(alert = alert,
                                      trigger_price = current_price,
                                      triggered_at = alert.triggered_at,
                                      triggered_method = alert.alert_type)
   
    logger.info('%s alert has triggered for {%s:%s}',alert.alert_type,alert.stock_symbol,alert.id)
    return True
      

def check_conditions(alert:Alert,current_price):
    """
    Return true if alert met the condition user provide 
    """
    if current_price is None:
        logger.warning('%s current price not founded!',alert.stock_symbol)
        return False
    
    result = (
    (alert.comparison == '>' and alert.target_price < current_price)or 
    (alert.comparison == '<' and alert.target_price > current_price)or 
    (alert.comparison == '=' and alert.target_price == current_price)
    ) and not alert.has_triggered
    
    if not result:
        logger.warning('%s alert conditions not satisfied yet for {%s:%s}',alert.alert_type,alert.stock_symbol,alert.id)    
    return result    