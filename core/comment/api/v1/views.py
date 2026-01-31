from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .permissions import IsOwner
from .paginations import DefaultPagination
from .serializers import CommentSerializers
from ...models import Comment
from blog.models import Post


class CommentCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializers
    pagination_class = DefaultPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
    
class CommentDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    queryset = Comment.objects.all()
