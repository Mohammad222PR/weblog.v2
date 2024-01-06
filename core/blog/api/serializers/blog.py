from blog.models import *
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ("slug", "is_public", "created_at", "updated_at", "is_membership")

    @staticmethod
    def validate_title(val):
        if val <= 3:
            raise serializers.ValidationError("Title must be 5 or more characters")
        return val

    @staticmethod
    def validate_description(val):
        if val <= 40:
            raise serializers.ValidationError("Description must be 40 characters")
        return val
