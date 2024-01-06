from blog.models import *
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField(source="absolute_url")
    # user = serializers.SlugRelatedField(slug_field="username")
    # category = serializers.SlugRelatedField()
    # tag = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = (
            "slug",
            "is_public",
            "created_at",
            "updated_at",
            "is_membership",
            "user",
        )

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            image = obj.image.url
            return request.build_absolute_uri(image)
        return None


    def get_comments(self, obj):
        serializers = CommentSerializer(instance=obj.comments.all(), many=True)
        return serializers.data
