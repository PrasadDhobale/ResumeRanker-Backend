# recruiter/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

from .models import User, Resume
from recruiter.models import Job
from ats.models import Application
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, ResumeSerializer
from ats.serializers import JobSerializer, ApplicationSerializer
from rest_framework.parsers import JSONParser
import secrets
import string
from django.utils import timezone
import base64

class UserRegisterView(APIView):
    def post(self, request):
        if request.method == 'POST':
            
            data = request.data

            # Check if the email already exists
            if User.objects.filter(email=data['email']).exists():
                return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Modify the request data to include the generated password
            # Set additional fields in the request data
            request_data = {
                'first_name': data['firstName'],
                'last_name': data['lastName'],
                'email': data['email'],
                'mobile_number': data['mobileNumber'],
                'password': data['password'],
                'verification_status': False,
                'registration_time': timezone.now(),
            }

            # Use the modified data to create the serializer
            serializer = UserSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email, password=password)
            serialized_user = UserSerializer(user).data
            return Response({'message': 'Login successful', 'user': serialized_user}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UploadResumeView(APIView):
    def post(self, request):
        if request.method == 'POST':
            
            data = request.data

            user = request.data.get('userId')
            title = request.data.get('title')
            resume_base64 = request.data.get('resume_base64')

            resume_id = ''.join(secrets.choice(string.digits) for _ in range(12))

            request_data = {
                'resume_id': resume_id,
                'user': user,
                'title': title,
                'resume_base64': resume_base64,
                'upload_time': timezone.now(),
            }

            # Use the modified data to create the serializer
            serializer = ResumeSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Resume Uploaded successfully', 'status':200}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)


class GetResume(APIView):
    def get(self, request, user_id):
        try:
            resumes = Resume.objects.filter(user_id=user_id)
            serializer = ResumeSerializer(resumes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resume.DoesNotExist:
            return Response({"error": "Resumes not found"}, status=status.HTTP_404_NOT_FOUND)

class ResumeDeleteView(APIView):
    
    def post(self, request, resume_id):
        try:
            resume = Resume.objects.get(pk=resume_id)
            resume.delete()
            return Response({"message": "Resume deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubmitApplicationView(APIView):
    
    def post(self, request):
        try:
            data = request.data
            userId = data.get('userId')
            resumeId = data.get('resumeId')
            jobId = data.get('jobId')
            matchingRate = data.get('rate')
                    
            application_id = ''.join(secrets.choice(string.digits) for _ in range(12))
            
            request_data = {
                'application_id' : application_id,
                'user': userId,
                'resume': resumeId,
                'job': jobId,
                'matching_rate': matchingRate,
                'apply_time': timezone.now(),
            }

            serializer = ApplicationSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'success': True, 'message': 'Application submitted successfully'})
            return JsonResponse({'success': False, 'error': serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class ApplyForJobView(APIView):
    def post(self, request, job_id):
        try:
            user_id = request.data.get('userId')
            job = Job.objects.get(pk=job_id)
            user = User.objects.get(pk=user_id)
            applied = Application.objects.filter(job=job, user=user).exists()
            return JsonResponse({'success': applied}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class GetResumeById(APIView):
    def get(self, request, resume_id):
        try:
            resume = Resume.objects.get(resume_id=resume_id)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)