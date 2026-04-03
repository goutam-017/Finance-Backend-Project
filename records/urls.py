from django.urls import path
from .views import *

urlpatterns = [
    path('records/', FinancialRecordView.as_view(), name='record-list-create'),
    path('records/<int:pk>', FinancialRecordDetailView.as_view(), name='record-detail'),
]