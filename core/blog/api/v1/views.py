from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .permissions import IsOwnerOrReadonly
from .serializers import PostSerializers
from ...models import Post

"""
API v1 inplementation using Function-Based Views.
Kept intentionally simple for educational comparison with cbv version.
"""

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def postList(request):
    """
    Displays list of blog posts and create posts.
    Access restricted to authenticated users.
    """
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsOwnerOrReadonly])
def postDetail(request, pk):
    """
    Retrieve, update or delete a single post instance.
    Access restricted to authenticated users and own author.
    """
    post = get_object_or_404(Post, id=pk)
    if request.method == "GET":
        serializer = PostSerializers(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializers(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail": "Item deleted!"}, status=status.HTTP_204_NO_CONTENT)
