from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadonly
from .serializers import PostSerializers, CategorySerializers
from ...models import Post, Category


class PostModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]
    serializer_class = PostSerializers
    queryset = Post.objects.all()
    pagination_class = DefaultPagination


class CategoryModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
