from blog.models import *
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostCategorySerializers(serializers.ModelSerializer):
    url_cat = serializers.SerializerMethodField(source="get_absolute_url")

    class Meta:
        model = Category
        fields = "__all__"

    def get_url_cat(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.pk)
        return None


class PostTagSerializers(serializers.ModelSerializer):
    url_tag = serializers.SerializerMethodField(source="get_absolute_url")

    class Meta:
        model = Tag
        fields = "__all__"

    def get_url_tag(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.pk)
        return None


class BlogSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(source="get_get_image")
    url_post = serializers.SerializerMethodField(source="get_absolute_url")
    author = serializers.StringRelatedField()
    snipes = serializers.ReadOnlyField()
    category = serializers.SlugRelatedField(
        many=False, slug_field="title", queryset=Category.objects.all()
    )
    tag = serializers.SlugRelatedField(
        many=True, slug_field="title", queryset=Tag.objects.all()
    )

    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = [
            "slug",
            "is_public",
            "created_at",
            "updated_at",
            "is_membership",
            "author",
        ]

    def get_url_post(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.pk)
        return None

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            image = obj.image.url
            return request.build_absolute_uri(image)
        return None

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        try:
            if request.parser_context.get("kwargs").get("pk"):
                rep.pop("snipes", None)
                rep.pop("url_post", None)
            else:
                rep.pop("body", None)
                rep.pop("comment", None)
                rep.pop("image", None)

            rep["tag"] = PostTagSerializers(instance.tag, many=True).data
            rep["category"] = PostCategorySerializers(instance.category).data
            return rep
        except:
            return None

    def get_comment(self, obj):
        try:
            ser = CommentSerializer(instance=obj.comments.all(), many=True)
            return ser.data
        except:
            return None
