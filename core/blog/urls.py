from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('post/', views.BlogListView.as_view(),name='blog-list'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('post/create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('post/<int:pk>/edit/', views.BlogEditView.as_view(), name='blog-edit'),
    path('post/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog-delete'),
    path('api/v1/', include('blog.api.v1.urls')),
    path('api/v2/', include('blog.api.v2.urls')),
]