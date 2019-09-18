from django.urls import path
from .views import LocationAPIView,ReportAPIView,TaskQueueAPIView,ReportOrCreateAPIView,TaskQueueGetTask,TestAPIView,ReportAPIView1,LibtechDataStatusAPIView
#GenericReportDetailAPIView,GenericReportUpdateAPIView,GenericReportCreateAPIView,GenericReportListAPIView

urlpatterns = [ 
                path('location/', LocationAPIView.as_view()),
                path('report/', ReportAPIView.as_view()),
                path('dataStatus/', LibtechDataStatusAPIView.as_view()),
                path('report1/', ReportAPIView1.as_view()),
                path('getReport/', ReportOrCreateAPIView.as_view()),
                path('queue/', TaskQueueAPIView.as_view()),
                path('getTask/', TaskQueueGetTask.as_view()),
                path('test/', TestAPIView.as_view()),
        ]

