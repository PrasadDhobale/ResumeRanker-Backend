from django.urls import path
from .views import MatchingRate;

urlpatterns = [
    path('matchingrate/', MatchingRate, name='matching-resume'),    
    # Add more URLs as needed
]
