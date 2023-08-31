from django.urls import path
from api.views import AttendanceStatusView
from api.views import AttendanceStats
from api.views import clientSelect,phaseSelect,Studentselect


urlpatterns = [
    path('api/attendance-status/', AttendanceStatusView.as_view(), name='attendance-status'),
    path('api/attendance-stats/', AttendanceStats.as_view(), name='AttendanceStats'),
    path('attendance/', clientSelect, name='Attendance'),
    path('studAtt/', phaseSelect, name='phaseAttendance'),
    path('get_students/', Studentselect.as_view(), name='StudentAttendance'),
    # Other URL patterns
]
