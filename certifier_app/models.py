from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    is_deleted = models.BooleanField(null=True)
    username = None

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        return super().save(*args , **kwargs) 


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

# Create your models here.
