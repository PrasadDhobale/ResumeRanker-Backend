# recruiter/serializers.py
from rest_framework import serializers
from .models import Recruiter
from .models import Job

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ('id', 'first_name', 'last_name', 'company_name', 'email', 'password', 'mobile_number', 'verification_status', 'registration_time')
        extra_kwargs = {'password': {'write_only': True}}

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('recruiter', 'job_id', 'title', 'description', 'skills', 'experience', 'no_of_openings', 'deadline', 'open_time')
        