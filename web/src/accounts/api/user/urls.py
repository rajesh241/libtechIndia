from django.urls import path
from .views import UserDetailAPIView
app_name = 'accountsUsers'

urlpatterns = [ 
                path('<username>/', UserDetailAPIView.as_view(),name='detail'),
             #   path('<username>/status/', UserCrawlQueueAPIView.as_view()),
        ]

