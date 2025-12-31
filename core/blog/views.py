from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .forms import PostForm

class BlogListView(ListView):
    model = Post
    paginate_by = 2
    ordering = '-created_date'

class BlogDetailView(DetailView):
    model = Post

class BlogCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm
    success_url = '/blog/post/'
