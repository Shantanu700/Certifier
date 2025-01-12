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

class Fonts(models.Model):
    font_name = models.CharField(max_length=50)
    font_file = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=0)

class Folders(models.Model):
    folder_name = models.CharField(max_length=50)
    folder_user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    parent = models.ForeignKey('self', null=True, on_delete=models.RESTRICT, related_name='child_folder')
    created_datetime = models.DateTimeField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(default=0)
    is_permanently_deleted = models.BooleanField(default=0)
    quickly_accessible = models.BooleanField(default=0)    
    is_starred = models.BooleanField(default=0) 

class Files(models.Model):
    def user_directory_path(instance, filename):
        print(instance.user.id)
        return "user_{0}/{1}".format(instance.user.id, filename)
    
    filename = models.CharField(max_length=50, null=True)
    file_size = models.CharField(max_length=10, null=True)
    file = models.FileField(upload_to=user_directory_path)
    created_datetime = models.DateTimeField(auto_now_add=True, null=True)
    parent_folder = models.ForeignKey(Folders, on_delete=models.RESTRICT, null=True)
    file_user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    is_deleted = models.BooleanField(default=0)
    is_permanently_deleted = models.BooleanField(default=0)
    quickly_accessible = models.BooleanField(default=0)    
    is_starred = models.BooleanField(default=0)



# Create your models here.
