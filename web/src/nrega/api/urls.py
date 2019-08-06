from django.urls import path
from .views import LocationAPIView,ReportAPIView,CrawlQueueAPIView,ReportOrCreateAPIView
#GenericReportDetailAPIView,GenericReportUpdateAPIView,GenericReportCreateAPIView,GenericReportListAPIView

urlpatterns = [ 
                path('location/', LocationAPIView.as_view()),
                path('report/', ReportAPIView.as_view()),
                path('getReport/', ReportOrCreateAPIView.as_view()),
                path('queue/', CrawlQueueAPIView.as_view()),
        ]

