from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from comment.forms import CommentForm
from .models import Post
from .forms import PostForm


class BlogListView(ListView):
    model = Post
    paginate_by = 2
    ordering = "-created_date"


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm
    success_url = "/blog/post/"


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = "/blog/post/"
