from django.urls import path
from api.views import AttendanceStatusView

urlpatterns = [
    path('api/attendance-status/', AttendanceStatusView.as_view(), name='attendance-status'),
    # Other URL patterns
]
