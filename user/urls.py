# user/urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, UserForgotPasswordView, UploadResumeView, GetResume, ResumeDeleteView, SubmitApplicationView
from .views import ApplyForJobView, GetResumeById, GetApplications, JobListView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('forgot-password/', UserForgotPasswordView.as_view(), name='user-forgot-password'),
    path('upload-resume/', UploadResumeView.as_view(), name='upload_resume'),
    path('resume/<int:user_id>/', GetResume.as_view(), name='get_resume'),
    path('resume/delete/<int:resume_id>/', ResumeDeleteView.as_view(), name='resume_detail'),
    path('application/', SubmitApplicationView.as_view(), name='submit_application'),
    path('apply/<int:job_id>/', ApplyForJobView.as_view(), name='apply_for_job'),
    path('getresume/<int:resume_id>/', GetResumeById.as_view(), name='get_resume_by_id'),
    path('applications/<int:user_id>/', GetApplications.as_view(), name='get_resume'),
    path('jobs/', JobListView.as_view(), name='job-list'),
]
