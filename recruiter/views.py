# recruiter/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Recruiter
from .models import Job  # Add this import statement

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

            # Generate a random password with 12 characters (you can adjust the length)
            random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

            # Modify the request data to include the generated password
            # Set additional fields in the request data
            request_data = {
                'first_name': data['firstName'],
                'last_name': data['lastName'],
                'company_name': data['companyName'],
                'email': data['email'],
                'mobile_number': data['mobileNumber'],
                'password': random_password,
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