from django.urls import path, re_path, include
from .views import (
    PostView,
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDestroyAPIView,
    )

# from rest_framework import routers

app_name = 'posts'

# router = routers.DefaultRouter()
# router.register('posts', PostView)
#
# urlpatterns = [
#     path('', include(router.urls))
# ]

urlpatterns = [
    re_path(r'^create/$', PostCreateAPIView.as_view(), name='post-create'),
    path('', PostListAPIView.as_view(), name='posts'),
    # re_path(r'^(?P<pk>[\d+]+)/$', PostDetailAPIView.as_view(), name='post-detail'),
    re_path(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='post-detail'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='post-update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', PostDestroyAPIView.as_view(), name='post-destroy'),

]
