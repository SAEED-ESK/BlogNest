from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from blog.models import Post
from .models import Comment
from .forms import CommentForm

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment/comment_create.html"
    success_url = "/comment/"

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, id=self.kwargs["post_id"])
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:blog-detail', kwargs={'pk': self.kwargs["post_id"]})

class CommentDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
    ):
    model = Comment
    template_name = "comment/comment_confirm_delete.html"
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_superuser
    
    def get_success_url(self):
        return reverse_lazy(
            'blog:blog-detail', kwargs={'pk': self.get_object().post.id}
        )

