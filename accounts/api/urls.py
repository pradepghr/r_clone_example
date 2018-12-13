from django.conf.urls import url

from .views import (
    UserCreateAPIView,
    UserLoginAPIView,

)

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
]