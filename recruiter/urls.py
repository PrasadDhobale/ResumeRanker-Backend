from django.urls import path
from .views import (
    RecruiterRegisterView,
    RecruiterLoginView,
    JobRegisterView,
    RecruiterJobsView,
    JobDetails,
    JobDelete
)

urlpatterns = [
    path('register/', RecruiterRegisterView.as_view(), name='recruiter_register'),
    path('login/', RecruiterLoginView.as_view(), name='recruiter_login'),
    path('create-job/', JobRegisterView.as_view(), name='create_job'),
    path('jobs/<int:recruiter_id>/', RecruiterJobsView.as_view(), name='recruiter-jobs'),
    path('job/<int:job_id>/', JobDetails.as_view(), name='job_details'),    
    path('job/delete/<int:recruiter_id>/<int:job_id>/', JobDelete.as_view(), name='job_delete'),  # Add URL for job deletion
    # Add more URLs as needed
]
