"""r_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls import static

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/auth/token/', obtain_jwt_token),
    path('api/users/', include('accounts.api.urls', namespace='users-api')),
    path('api/posts/', include('posts.api.urls', namespace='posts-api')),
    # path('', include('posts.api.urls', namespace='posts-api')),
    path('api/comments/', include('comments.api.urls', namespace='comments-api')),

]
