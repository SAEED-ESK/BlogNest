from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm

class BlogListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 2
    ordering = '-created_date'

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Post

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm
    success_url = '/blog/post/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class BlogEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm
    success_url = '/blog/post/'
    
class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = '/blog/post/'
    
