from django.urls import path
from api.views import AttendanceStatusView
from api.views import AttendanceStats

urlpatterns = [
    path('api/attendance-status/', AttendanceStatusView.as_view(), name='attendance-status'),
    path('api/attendance-stats/', AttendanceStats.as_view(), name='AttendanceStats'),

    # Other URL patterns
]
