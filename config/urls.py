from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def root(request):
    return Response({
        "message": "Finance Backend API is running!",
        "version": "v1",
        "endpoints": {
            "register"          : "/api/auth/register/",
            "login"             : "/api/auth/login/",
            "user_profile"      : "/api/auth/user_profile/",
            "new_access_token"  : "/api/auth/new_access_token/",
            "users"             : "/api/auth/users/<id>/",
            "records"           : "/api/records/",
            "dashboard"         : "/api/dashboard/summary/",
            "docs"              : "/api/docs/",
            "admin"             : "/admin/",
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root),
    path('api/auth/', include('users.urls')),
    path('api/', include('records.urls')),
    path('api/', include('dashboard.urls')),
]