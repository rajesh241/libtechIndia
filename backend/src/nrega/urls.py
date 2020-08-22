"""URL Definations for API Views"""
from django.urls import path
from .views import (
    LocationAPIView, 
    LibtechTagAPIView,
)

urlpatterns = [ 
                path('location/', LocationAPIView.as_view()),
                path('tag/', LibtechTagAPIView.as_view()),
        ]

