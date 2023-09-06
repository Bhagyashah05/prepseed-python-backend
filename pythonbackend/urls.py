from django.urls import path
from api.views import AttendanceStatusView
from api.views import AttendanceStats
from api.views import clientSelect,phaseSelect
from api.views import StudentAttendanceAnalysis,Studentselect
from chatanalysis.views import chatAnalysis,chatHtml

urlpatterns = [
    path('api/attendance-status/', AttendanceStatusView.as_view(), name='attendance-status'),
    path('api/attendance-stats/', AttendanceStats.as_view(), name='AttendanceStats'),
    path('attendance/', clientSelect, name='Attendance'),
    path('studAtt/', phaseSelect, name='phaseAttendance'),
    path('get_students/', Studentselect.as_view(), name='StudentAttendance'),
    path('studentAttendanceAnalysis/',StudentAttendanceAnalysis.as_view(),name='StudentAttendanceAnalysis'),
    path('api/chatAnalysis/',chatAnalysis.as_view(),name='chatAnalysis'),
    path('chatanalysis/',chatHtml,name='chatHtml')


    # Other URL patterns
]