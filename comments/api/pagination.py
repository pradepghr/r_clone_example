from rest_framework.pagination import PageNumberPagination


class CommentPageNumberPagination(PageNumberPagination):
    page_size = 5
