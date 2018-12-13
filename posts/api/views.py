from django.db.models import Q

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .permissions import IsOwnerOrReadOnly

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

# from rest_framework.pagination import (
#     LimitOffsetPagination,
#     PageNumberPagination,
# )

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

from rest_framework.viewsets import ModelViewSet

from .serializers import PostSerializer, PostDetailSerializer
from posts.models import Post


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListAPIView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]  # provided by rest_framework e.g http://127.0.0.1:8000/api/posts/?search=test
    search_fields = ['title', 'content']   # e.g http://127.0.0.1:8000/api/posts/?search=test&ordering=id

    # pagination_class = PageNumberPagination   # default from rest framework
    # pagination_class = LimitOffsetPagination  # e.g http://127.0.0.1:8000/api/posts/?limit=2
    # pagination_class = PostLimitOffsetPagination  # custom LimitOffsetPagination
    pagination_class = PostPageNumberPagination     # custom PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        # queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
            ).distinct()
        return queryset_list


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'xyz'


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
