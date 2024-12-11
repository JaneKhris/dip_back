"""
URL configuration for project_users project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from files.views import FileViewSet
from users.views import register, UserViewSet, CustomAuthToken, logout
from rest_framework.routers import DefaultRouter
from settings.views import get_path, get_response
from files.views import preview, download, download_url

router_files = DefaultRouter()
router_files.register('files', FileViewSet)

router_users = DefaultRouter()
router_users.register('users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register),
    # path('api/', include('djoser.urls.authtoken')),
    path('api/', include(router_files.urls)),
    path('api/', include(router_users.urls)),
    path('start/', get_path),
    path('res/', get_response),
    path('api/auth/login/', CustomAuthToken.as_view()),
    path('api/auth/logout/', logout),
    path('api/preview/', preview),
    path('api/download/<file_id>/', download),
    path('api/storage/<str>/',download_url)
]
