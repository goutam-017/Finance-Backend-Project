from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import FinancialRecord
from rest_framework.pagination import PageNumberPagination
from .serializers import FinancialRecordSerializer
from users.permissions import *
from django.db.models import Q

# Create your views here.
class FinancialRecordView(APIView):
    def get_permissions(self):
        if self.request.method=='GET':
            return [IsAnyRole()]
        return [IsAdmin()]

    def get(self,request):
        queryset=FinancialRecord.objects.filter(is_deleted=False)

        record_type = request.query_params.get('type')
        category = request.query_params.get('category')
        date = request.query_params.get('date')
        search = request.query_params.get('search')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        ordering = request.query_params.get('ordering', '-date')

        if(record_type):
            queryset=queryset.filter(type=record_type)
        if(category):
            queryset=queryset.filter(category__icontains=category)
        if(date):
            queryset=queryset.filter(date=date)
        if(search):
            queryset=queryset.filter(Q(category__icontains=search) | Q(description__icontains=search))
        if(date_from):
            queryset = queryset.filter(date__gte=date_from)
        if(date_to):
            queryset = queryset.filter(date__lte=date_to)

        allowed_orderings=['date', '-date', 'amount', '-amount']
        if(ordering in allowed_orderings):
            queryset=queryset.order_by(ordering)

        paginator=PageNumberPagination()
        paginator.page_size=10
        paginated_qs=paginator.paginate_queryset(queryset,request)
        serializer=FinancialRecordSerializer(paginated_qs,many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self,request):
        data=request.data
        serializer=FinancialRecordSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save(created_by=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class FinancialRecordDetailView(APIView):
    def get_permissions(self):
        if(self.request.method=='GET'):
            return [IsAnyRole()]
        return [IsAdmin()]

    def get_object(self,pk):
        return get_object_or_404(FinancialRecord,pk=pk,is_deleted=False)

    def get(self,request,pk):
        record=self.get_object(pk)
        serializer=FinancialRecordSerializer(record)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        record=self.get_object(pk)
        serializer=FinancialRecordSerializer(record,data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        record=self.get_object(pk)
        serializer=FinancialRecordSerializer(record,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        record=self.get_object(pk)
        record.is_deleted=True
        record.save()
        return Response({'msg':'Record deleted.'},status=status.HTTP_200_OK)