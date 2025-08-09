from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin,AbstractUser 
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length = 30, unique = True,
                            validators=[RegexValidator(r'^[a-zA-Z0-9][a-zA-Z0-9_]{2,29}$',
                                                       'doesn\'t allow special characters except ( _ ). Username length ranging(3-30).')])
    phone_num = models.CharField(max_length = 20, unique = True, 
                                 validators = [RegexValidator(r'^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$','international dialing code at the start and digits only.')])
    email = models.EmailField(unique = True)
    
    #log_out = models.DateTimeField(null = True, blank = True)
    
    def __str__(self):
        return self.username