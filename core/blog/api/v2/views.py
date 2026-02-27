from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadonly
from .serializers import PostSerializers, CategorySerializers
from ...models import Post, Category

"""
API v2 implementaion for managing blog posts.
Provides full CRUD functionality using DRF ModelViewSets.
"""

class PostModelViewSet(ModelViewSet):
    # Read access in public; write access is limited to the post owner
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]
    serializer_class = PostSerializers
    queryset = Post.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class CategoryModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
