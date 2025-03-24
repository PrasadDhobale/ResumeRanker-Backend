# User/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
import base64

class User(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # You may want to use a more secure field like PasswordField
    mobile_number = models.CharField(max_length=15)  # Adjust the max_length as needed
    
    verification_status = models.BooleanField(default=False)
    registration_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Resume(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    resume_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=255)
    resume_base64 = models.TextField()  # Using TextField to store base64-encoded data
    upload_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.resume_id