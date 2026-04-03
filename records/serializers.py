from rest_framework import serializers
from .models import *

class FinancialRecordSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = FinancialRecord
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'is_deleted']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value