# recruiter/urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, UploadResumeView, GetResume

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('upload-resume/', UploadResumeView.as_view(), name='upload_resume'),
    path('resume/<int:user_id>/', GetResume.as_view(), name='get_resume'),
]
