from django.urls import path, include
from . import views

app_name = "comment"

urlpatterns = [
    path("add/<int:post_id>", views.CommentCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", views.CommentDeleteView.as_view(), name="delete"),
    path("api/v1/", include("comment.api.v1.urls")),
]
