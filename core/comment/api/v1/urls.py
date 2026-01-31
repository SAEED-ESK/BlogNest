from django.urls import path, include
from . import views

app_name = "api-v1"

urlpatterns = [
    path("post/<int:post_id>/comments/", views.CommentCreateAPIView.as_view(), name="post-comments"),
    path("delete/<int:pk>/", views.CommentDeleteAPIView.as_view(), name="api-delete"),
]
