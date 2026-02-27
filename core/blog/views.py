from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404

from comment.forms import CommentForm
from .models import Post, Category
from .forms import PostForm
from accounts.models import Profile


class BlogListView(ListView):
    """
    Displays the list of blog posts with True status
    """
    model = Post
    paginate_by = 2
    ordering = "-created_date"

    def get_queryset(self):
        queryset = super().get_queryset().filter(status=True)
        category_name = self.request.GET.get('category')
        if category_name:
            self.category = get_object_or_404(Category, name=category_name)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.category
        return context


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the detail page of a blog post.
    Only for authenticated users.
    """
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """
        Injects the comment form into the template contenxt.
        """
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    """
    Create a post for authenticated user.
    """
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        """
        Add user instance of post automatically from request data.
        """
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class BlogEditView(LoginRequiredMixin, UpdateView):
    """
    Edit a blog post by own author.
    After success editing redirect to list of blog posts
    """
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm

    def get_queryset(self):
        author = Profile.objects.get(user=self.request.user)
        return super().get_queryset().filter(author=author)
    
    def get_success_url(self):
        return reverse("blog:blog-detail", kwargs={"pk": self.object.id})

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a blog post by own author.
    After success editing redirect to list of blog posts
    """
    model = Post
    template_name = "blog/post_delete.html"
    success_url = "/blog/post/"

    def get_queryset(self):
        author = Profile.objects.get(user=self.request.user)
        return super().get_queryset().filter(author=author)
