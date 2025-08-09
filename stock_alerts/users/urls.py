from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_blacklist
from .views import register_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('register/me', register_user, name='my-info'),
    path('token/', token_obtain_pair, name='applyToken'),
    path('token/refresh/', token_refresh , name='refreshToken'),
    path('token/block/', token_blacklist , name='blackList'),
]