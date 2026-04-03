from .serializers import *
from .permissions import *
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        data=request.data.copy()
        data['role'] = 'viewer'
        serializer=UserSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'msg':'Registration Successfully.'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        data=request.data
        username=data.get('username')
        password=data.get('password')

        if(not username or not password):
            return Response({'msg':'Username and password are required.'},status=status.HTTP_400_BAD_REQUEST)

        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'msg':'Invalid Credentials.'},status=status.HTTP_400_BAD_REQUEST)

        if(not user.check_password(password)):
            return Response({'msg':'Invalid Credentials.'},status=status.HTTP_400_BAD_REQUEST)

        if(not user.is_active):
            return Response({'msg':'Your account has been deactivated.'},status=status.HTTP_403_FORBIDDEN)

        refresh=RefreshToken.for_user(user=user)
        return Response({
            'msg': 'Login Successfully.',
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        },status=status.HTTP_200_OK)
    

class NewAccessToken(APIView):
    def post(self,request):
        refresh_token=request.data.get('refresh_token')
        if(not refresh_token):
            return Response({'msg':'Refresh token is required.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh=RefreshToken(refresh_token)
            new_access_token=str(refresh.access_token)
            return Response({'access_token':new_access_token},status=status.HTTP_200_OK)
        except TokenError:
            return Response({'msg':'Invalid or expired refresh token'},status=status.HTTP_401_UNAUTHORIZED)
        

class UserProfile(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        userdata={
            "id":user.id,
            "username": user.username,
            "email": user.email,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "role":user.role,
        }
        return Response(userdata,status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes=[IsAdmin]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail=f"User with id '{pk}' not found.")

    def put(self,request,pk):
        user=self.get_object(pk)
        serializer=UserSerializer(user,data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        user=self.get_object(pk)
        serializer=UserSerializer(user,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'msg':'User Updated Successfully.','data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        user=self.get_object(pk)
        if(user.role=='admin' and user.is_staff):
            return Response({'msg':"Admins accounts cannot be deactivated."},status=status.HTTP_403_FORBIDDEN)
        user.is_active=False
        user.save()
        return Response({'msg':'User deactivated.'},status=status.HTTP_200_OK)