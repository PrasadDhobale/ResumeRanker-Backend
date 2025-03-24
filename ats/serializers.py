# ats/serializers.py
from rest_framework import serializers
from user.models import User, Resume
from recruiter.models import Job
from .models import Application, Selection

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'skills', 'experience', 'no_of_openings', 'deadline')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'mobile_number', 'verification_status', 'registration_time')
        extra_kwargs = {'password': {'write_only': True}}

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('resume_id', 'user', 'title', 'resume_base64', 'upload_time')
        extra_kwargs = {'resume_base64': {'write_only': True}}


class ApplicationSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Application
        fields = ('application_id', 'user', 'resume', 'job', 'matching_rate', 'apply_time')


class SelectionSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Selection
        fields = ('selection_id', 'application', 'selection_time')
