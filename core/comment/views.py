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
    """
    Create a comment by its author.
    Redirects to the related blog post detail page after deletion.
    """
    model = Comment
    form_class = CommentForm
    template_name = "comment/comment_create.html"
    success_url = "/comment/"

    def form_valid(self, form):
        """
        Validation form of new comment.
        Automatically assign comment's author from request content.
        """
        form.instance.post = get_object_or_404(Post, id=self.kwargs["post_id"])
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the parent post detail page after successful deletion.
        """
        return reverse('blog:blog-detail', kwargs={'pk': self.kwargs["post_id"]})

class CommentDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
    ):
    """
    Allow deletion of a comment by its author or a superuser.
    Redirects to the related blog post detail page after deletion.
    """
    model = Comment
    template_name = "comment/comment_confirm_delete.html"

    def test_func(self):
        """
        Restrict deletion access to the comment author or superusers.
        """
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_superuser
    
    def get_success_url(self):
        """
        Redirect to the parent post detail page after successful deletion.
        """
        return reverse_lazy(
            'blog:blog-detail', kwargs={'pk': self.get_object().post.id}
        )

