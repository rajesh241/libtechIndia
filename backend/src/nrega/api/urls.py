"""URL Definations for API Views"""
from django.urls import path
from .views import LocationAPIView, ReportAPIView, LibtechTagAPIView

urlpatterns = [ 
                path('location/', LocationAPIView.as_view()),
                path('report/', ReportAPIView.as_view()),
                path('tag/', LibtechTagAPIView.as_view()),
        ]

