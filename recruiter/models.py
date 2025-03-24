# recruiter/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Recruiter(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # You may want to use a more secure field like PasswordField
    mobile_number = models.CharField(max_length=15)  # Adjust the max_length as needed
    
    verification_status = models.BooleanField(default=False)
    registration_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
        

class Job(models.Model):
    recruiter = models.ForeignKey('Recruiter', on_delete=models.CASCADE)
    
    job_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.CharField(max_length=255)
    experience = models.IntegerField()
    no_of_openings = models.IntegerField()
    deadline = models.DateTimeField()
    open_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_id

