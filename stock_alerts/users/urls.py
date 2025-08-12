from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_blacklist
from .views import register_user, notification_setting_update

urlpatterns = [
    # user endpoints
    path('register', register_user, name='register'),
    path('me', register_user, name='my-info'),
    # notificaitions endpoints
    path('me/notification-settings', notification_setting_update, name='update-settings'),
    # token endpoints
    path('token/', token_obtain_pair, name='applyToken'),
    path('token/refresh/', token_refresh , name='refreshToken'),
    path('token/block/', token_blacklist , name='blackList'),
]