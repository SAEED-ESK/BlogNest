from django.db import models
from django.contrib.auth import get_user_model

# getting user model object
User = get_user_model()


class Post(models.Model):
    """
    Represents a blog post a authored by a user.
    Handles Contents, publication state, and categorization.
    """
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
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


class Category(models.Model):
    """
    Represents a category related to posts.
    """
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
