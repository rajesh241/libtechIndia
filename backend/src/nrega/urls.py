"""URL Definations for API Views"""
from django.urls import path
from .views import (
    LocationAPIView, 
    LibtechTagAPIView,
)
import nrega.views as views

urlpatterns = [ 
                path('location/', views.LocationAPIView.as_view()),
                path('taglocations/', views.TagLocationsAPIView.as_view()),
                path('tag/', views.LibtechTagAPIView.as_view()),
        ]

