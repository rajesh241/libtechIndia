"""URL Configuration for User App"""
from django.urls import path, include, re_path
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user import views
from user import psa_views
router = routers.DefaultRouter()
router.register('profile', views.ModifyUserView)

app_name = 'user'

urlpatterns = [
    re_path(r'social/(?P<backend>[^/]+)/$', psa_views.exchange_token),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('modify/', include(router.urls)),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('activate/', views.UserActivateView.as_view(), name='user_activate_view'),
    path('', views.UserAPIView.as_view(), name='user_api_view'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('otp/', views.OTPAPIView.as_view(), name='otp_view'),
    path('bulkcreate/', views.BulkUserAPIView.as_view(), name='bulk_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bulkdelete/', views.UserBulkDeleteView.as_view(), name='bulk_delete'),
#    path('password_reset/', include('django_rest_passwordreset.urls',
#                                             namespace='password_reset')),

]
