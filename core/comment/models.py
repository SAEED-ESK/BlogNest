from django.db import models
from blog.models import Post
from django.contrib.auth import get_user_model

# getting user model object
User = get_user_model()


class Comment(models.Model):
    """
    Represents a comment of a post by a user.
    Handles Contents.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_date"]

    def __str__(self):
        """
        Show comment body and author name.
        """
        return "Comment {} by {}".format(self.body, self.name)
