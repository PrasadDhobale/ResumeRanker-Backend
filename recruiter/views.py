# recruiter/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Recruiter
from ats.models import Application
from .models import Job  # Add this import statement
from django.shortcuts import get_object_or_404
from ats.serializers import ApplicationSerializer
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password

from .serializers import RecruiterSerializer
from .serializers import JobSerializer

import secrets
import string
from django.utils import timezone

class RecruiterRegisterView(APIView):
    def post(self, request):
        if request.method == 'POST':
            
            data = request.data

            # Check if the email already exists
            if Recruiter.objects.filter(email=data['email']).exists():
                return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

            # Modify the request data to include the generated password
            # Set additional fields in the request data
            request_data = {
                'first_name': data['firstName'],
                'last_name': data['lastName'],
                'company_name': data['companyName'],
                'email': data['email'],
                'mobile_number': data['mobileNumber'],
                'password': data['password'],
                'verification_status': False,
                'registration_time': timezone.now(),
            }

            # Use the modified data to create the serializer
            serializer = RecruiterSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Recruiter registered successfully'}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)

class RecruiterLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            recruiter = Recruiter.objects.get(email=email, password=password)
            serialized_recruiter = RecruiterSerializer(recruiter).data
            return Response({'message': 'Login successful', 'recruiter': serialized_recruiter}, status=status.HTTP_200_OK)
        except Recruiter.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RecruiterForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        try:
            recruiter = Recruiter.objects.get(email=email)
         
            email_html = render_to_string('forgot_password.html', {'password': recruiter.password, 'name': recruiter.first_name})

            send_mail(
                subject='Password Reset Request', 
                message="Your application has been selected!",             
                html_message=email_html,
                from_email='services.propad@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({'message': 'Temporary password sent to your email'}, status=status.HTTP_200_OK)
        except Recruiter.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)


class JobRegisterView(APIView):
    def post(self, request):
        if request.method == 'POST':
            
            data = request.data

            # Modify the request data to include additional fields
            jobId = ''.join(secrets.choice(string.digits + string.digits) for _ in range(12))
            request_data = {
                'recruiter': data['recruiterId'],
                'job_id': jobId,
                'title': data['title'],
                'description': data['description'],
                'skills': data['skills'],
                'experience': data['experience'],
                'no_of_openings': data['noOfOpenings'],
                'deadline': data['deadline'],
                'open_time': timezone.now(),
            }

            # Use the modified data to create the serializer
            serializer = JobSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Job Created successfully', 'status': 200}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class RecruiterJobsView(APIView):
    def get(self, request, recruiter_id):
        jobs = Job.objects.filter(recruiter_id=recruiter_id)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobDetails(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(job_id=job_id)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

class JobDelete(APIView):
    def post(self, request, recruiter_id, job_id):
        try:
            job = Job.objects.get(job_id=job_id, recruiter_id=recruiter_id)
            job.delete()
            return Response({"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

class GetApplicantCount(APIView):
    def post(self, request, recruiter_id, job_id):
        try:
            job = Job.objects.get(pk=job_id, recruiter_id=recruiter_id)
            applicant_count = Application.objects.filter(job=job).count()
            return JsonResponse({'applicant_count': applicant_count}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)


class GetAllApplicantDetails(APIView):
    def post(self, request, recruiter_id, job_id):
        job = get_object_or_404(Job, pk=job_id, recruiter_id=recruiter_id)
        
        applications = Application.objects.filter(job=job)
        
        serializer = ApplicationSerializer(applications, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)