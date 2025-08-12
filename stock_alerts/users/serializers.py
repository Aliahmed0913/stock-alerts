from rest_framework import serializers
from .models import User, UserNotificationSetting

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8, max_length=15)
    
    class Meta():
        model = User
        fields = ['username', 'email', 'phone_num', 'password']
    
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        UserNotificationSetting.objects.create(user = user)
        return user
    

class UserNotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    
    class Meta():
        model = UserNotificationSetting
        fields = ['user', 'enable_email', 'cooldown_period', 'last_notified']