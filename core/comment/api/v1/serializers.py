from rest_framework import serializers
from ...models import Comment
from accounts.models import User


class CommentSerializers(serializers.ModelSerializer):
    """
    Serializer for Comment Model.
    Handles dynamic fields, absolute URL generation
    and author assignment based on request context.
    """
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "body",
            "absolute_url",
            "created_date",
        ]
        read_only_fields = ["author", "post"]

    def get_absolute_url(self, obj):
        """
        Builds an absolute URL for the post detail endpoints.
        Used in list views for client-side navigation.
        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        """
        Customize API output based on request context.
        - In detail view: hide absolute_url
        """
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("absolute_url", None)
        return rep

    def create(self, validated_data):
        """
        Automatically assign the authenticated user's profile as the author of the post.
        """
        request = self.context.get("request")
        validated_data["author"] = User.objects.get(id=request.user.id)
        return super().create(validated_data)
