from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path("post/", views.postList, name="blog-list"),
    path("post/<int:pk>/", views.postDetail, name="blog-detail"),
]
