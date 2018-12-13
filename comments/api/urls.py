from django.urls import path, re_path
from django.contrib import admin

from .views import (
    CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
)

app_name = 'comments'

urlpatterns = [
    re_path(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    path('', CommentListAPIView.as_view(), name='list'),
    re_path(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),

]
