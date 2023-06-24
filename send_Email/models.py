from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Email_this(models.Model):
    to = models.CharField(max_length=255,default='not_null')
    subject = models.CharField(max_length=255,default='null')
    message = models.TextField(blank=True,default='null')
    filee = models.FileField(default='null') 
    
    def delete(self, *args, **kwargs):
        self.filee.delete()
        super().delete(*args, **kwargs)
    