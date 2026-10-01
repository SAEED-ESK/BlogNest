from django.db import models
from django.contrib.auth import get_user_model
from django.templatetags.static import static

from core import settings

# getting user model object
User = get_user_model()


class Post(models.Model):
    """
    Represents a blog post a authored by a user.
    Handles Contents, publication state, and categorization.
    """
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="posts/")
    title = models.CharField(max_length=250)
    content = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    # Indicates whether the post is published or still in draft state
    status = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # Explicit publish time, independent of creation time
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return static("images/default-post.jpg")


class Category(models.Model):
    """
    Represents a category related to posts.
    """
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
