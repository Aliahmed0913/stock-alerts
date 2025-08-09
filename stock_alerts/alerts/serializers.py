from rest_framework import serializers,validators
from .models import Alert, TriggeredAlert
from datetime import timedelta
from stock_alerts.settings import STOCK_SYMBOLS
from decimal import Decimal
class AlertReadSerializer(serializers.ModelSerializer):
    class Meta():
        model = Alert
        fields = ['id','user','stock_symbol','alert_type','comparison',
                  'target_price','duration','is_active','has_triggered',
                  'triggered_at','created_at']
        
        read_only_fields = fields
      

class AlertCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    
    class Meta():
        model = Alert
        fields = ['id','user','stock_symbol','alert_type','comparison',
                  'target_price','duration','is_active','has_triggered',
                  'triggered_at','created_at']
        
        read_only_fields = ['is_active','has_triggered',
                            'triggered_at','created_at','user']
   
    def validate(self, attrs):
        user = self.context['request'].user
        alert_type = attrs.get('alert_type').strip().lower()
        symbol = attrs.get('stock_symbol').strip().upper()
        target_price = Decimal(attrs.get('target_price'))
        comparison = attrs.get('comparison')
        duration = attrs.get('duration')
        
        if target_price <= 0 :
            raise serializers.ValidationError({'Price_issue':'Your target price can\'t be zero or less.'}) 
                     
        if symbol not in STOCK_SYMBOLS:
            raise serializers.ValidationError({'Stock_symbol':'Unsupported stock symbol.!'})
        
        if alert_type == 'threshold' :
            attrs['duration'] = timedelta(0)
        
        alert_conditions = {
        'user': user,
        'stock_symbol': symbol,
        'comparison': comparison,
        'target_price': target_price,
        }
        
        if alert_type == 'duration':
            alert_conditions['duration'] = duration  
        
        existing_alerts = Alert.objects.filter(**alert_conditions)
         
        if self.instance:
            existing_alerts = existing_alerts.exclude(pk = self.instance.pk)
            
        if existing_alerts.exists():
            raise serializers.ValidationError({
                "Duplication_issue": f"You already have an alert for {symbol}."
            })
            
            
        return attrs
    
    def create(self, validated_data):      
        return Alert.objects.create(user = self.context['request'].user, 
        alert_type = validated_data['alert_type'].strip().lower(),
        stock_symbol = validated_data['stock_symbol'].strip().upper(),
        target_price = Decimal(validated_data['target_price']),
        comparison = validated_data['comparison'],
        duration = validated_data['duration'])
    
                                                    
                                                    
class TriggeredAlertSerializer(serializers.ModelSerializer):
    alert_id = serializers.IntegerField(source = 'alert.id', read_only = True)
    class Meta():
        model = TriggeredAlert
        fields = ['alert_id', 'trigger_price', 'triggered_at', 'triggered_method']