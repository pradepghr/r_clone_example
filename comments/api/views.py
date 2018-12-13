from django.db.models import Q

from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from comments.api.permissions import IsOwnerOrReadOnly

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from comments.api.pagination import CommentPageNumberPagination

from .serializers import CommentListSerializer, CommentDetailSerializer, create_comment_serializer
from comments.models import Comment


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )

    # 127.0.0.1:8000/api/comments/create/?type=post
    # http://127.0.0.1:8000/api/comments/create/?type=post&slug=test-permission
    # 127.0.0.1:8000/api/comments/create/?type=post&slug=test-permission&parent_id=7


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content']
    pagination_class = CommentPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query)
            ).distinct()
        return queryset_list


class CommentDetailAPIView(RetrieveAPIView, UpdateModelMixin, DestroyModelMixin):
    queryset = Comment.objects.filter(id__gte=0)  # because comment.objects.all() gives only for parent = None
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
