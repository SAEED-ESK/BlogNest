from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post/', views.BlogListView.as_view(),name='blog-list'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('post/create/', views.BlogCreateView.as_view(), name='blog-create'),
]