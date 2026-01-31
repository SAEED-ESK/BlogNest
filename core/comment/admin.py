from django.contrib import admin
from .models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "body",
        "post",
        "user_email",
        "created_date",
    )
    list_filter = ("created_date",)
    search_fields = ("name", "body")

    def user_email(self, obj):
        return obj.author.email


admin.site.register(Comment, CommentAdmin)
