from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    published_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Post
        fields = [
            "image",
            "title",
            "content",
            "category",
            "status",
            "published_date",
        ]