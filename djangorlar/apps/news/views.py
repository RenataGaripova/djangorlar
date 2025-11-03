import datetime

from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import Article, Category, Tag, Comment
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateUpdateSerializer,
    CategorySerializer,
    TagSerializer,
    CommentSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 345


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission: safe methods allowed for everyone, write for admins only."""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related("category", "author").prefetch_related("tags")
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ("category__slug", "tags__slug", "author__id", "published")
    search_fields = ("title", "summary", "content")
    ordering_fields = ("publish_at", "created_at")
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ("list",):
            return ArticleListSerializer
        if self.action in ("retrieve",):
            return ArticleDetailSerializer
        return ArticleCreateUpdateSerializer

    def get_queryset(self):
        qs = self.queryset
        # if not admin, only show published articles
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(published=True, publish_at__lte=datetime.datetime.now())
        return qs

    @action(detail=False, methods=["get", "post"], url_path="featured")
    def featured(self, request):
        featured_qs = self.get_queryset().filter(is_featured=True)[:10]
        page = self.paginate_queryset(featured_qs)
        serializer = ArticleListSerializer(page, many=True, context={"request":request})
        return self.get_paginated_response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
