from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password','role','is_active']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)