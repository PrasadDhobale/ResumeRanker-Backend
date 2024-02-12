# recruiter/serializers.py
from rest_framework import serializers
from .models import User, Resume
import base64

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'mobile_number', 'verification_status', 'registration_time')
        extra_kwargs = {'password': {'write_only': True}}


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('resume_id', 'user', 'title', 'resume_base64', 'upload_time')
        extra_kwargs = {'resume_file': {'write_only': True}}