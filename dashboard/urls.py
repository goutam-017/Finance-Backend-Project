from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/summary/', DashboardSummaryView.as_view(),name='dashboard_summary'),
]