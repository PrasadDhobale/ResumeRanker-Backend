from django.urls import path
from .views import MatchingRateView, GetSelectedApplicants, SelectionView, UnSelectView

urlpatterns = [
    path('matchingrate/', MatchingRateView.as_view(), name='matching-resume'),
    path('selection/<int:job_id>/', GetSelectedApplicants.as_view(), name='get_selected_applicants'),
    path('selection/', SelectionView.as_view(), name='select-application'),    
    path('unselect/', UnSelectView.as_view(), name='unselect-application'),
    
    # Add more URLs as needed
]
