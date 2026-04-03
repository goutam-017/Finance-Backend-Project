from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('user_profile/',UserProfile.as_view(),name='user_profile'),

    # this api endpoint for regenerate new access token
    path('new_access_token/',NewAccessToken.as_view(),name='new_access_token'),

    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]