from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError("Password is not mach")

        try:
            validate_password(attrs.get("password"))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.message)})

        return super().validate(attrs)

    def create(self, validated_data):
        serializers.pop("password1", None)
        return User.objects.create(**validated_data)


class ResendActivationCodeSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=200)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError({"details": "user does not exist"})

        if user_obj.is_verified:
            raise serializers.ValidationError({"details": "you already have verified"})

        attrs["user"] = user_obj
        return super().validate(attrs)
