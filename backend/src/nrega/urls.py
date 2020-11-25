"""URL Definations for API Views"""
from django.urls import path, include
from rest_framework import routers
from .views import (
    LocationAPIView, 
    LibtechTagAPIView,
)
import nrega.views as views

router = routers.DefaultRouter()
router.register('bundle', views.BundleViewSet, basename="bundle")
urlpatterns = [
                path('', include(router.urls)),
                path('location/', views.LocationAPIView.as_view()),
                path('report/', views.ReportAPIView.as_view()),
                path('reportagg/', views.ReportAggAPIView.as_view()),
                path('taglocations/', views.TagLocationsAPIView.as_view()),
                path('queue/', views.TaskQueueAPIView.as_view()),
                path('tag/', views.LibtechTagAPIView.as_view()),
        ]

