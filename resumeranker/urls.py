# recruiter_backend/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recruiter/', include('recruiter.urls')),
    path('user/', include('user.urls')),
    path('ats/', include('ats.urls')),
    # Add more URLs as needed
]
