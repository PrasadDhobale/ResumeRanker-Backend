from django.urls import path
from .views import (
    RecruiterRegisterView,
    RecruiterLoginView,
    RecruiterForgotPasswordView,
    JobRegisterView,
    RecruiterJobsView,
    JobDetails,
    JobDelete,
    GetApplicantCount,
    GetAllApplicantDetails,
)

urlpatterns = [
    path('register/', RecruiterRegisterView.as_view(), name='recruiter_register'),
    path('login/', RecruiterLoginView.as_view(), name='recruiter_login'),
    path('forgot-password/', RecruiterForgotPasswordView.as_view(), name='recruiter-forgot-password'),
    path('create-job/', JobRegisterView.as_view(), name='create_job'),
    path('jobs/<int:recruiter_id>/', RecruiterJobsView.as_view(), name='recruiter-jobs'),
    path('job/<int:job_id>/', JobDetails.as_view(), name='job_details'),
    path('job/delete/<int:recruiter_id>/<int:job_id>/', JobDelete.as_view(), name='job_delete'),
    path('job/getapplicationcount/<int:recruiter_id>/<int:job_id>/', GetApplicantCount.as_view(), name='applicantCount'),
    path('job/getapplicantdetails/<int:recruiter_id>/<int:job_id>/', GetAllApplicantDetails.as_view(), name='applicantDetails'),
]
