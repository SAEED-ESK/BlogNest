from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializers(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "image",
            "content",
            "status",
            "category",
            "author",
            "absolute_url",
            "published_date",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context["request"]
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySerializers(
            instance.category, context={"request": request}
        ).data
        return rep

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = Profile.objects.get(user__id=request.user.id)
        return super().create(validated_data)
