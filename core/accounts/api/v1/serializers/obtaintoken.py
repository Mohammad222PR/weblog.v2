from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_verified:
                raise serializers.ValidationError(
                    {"detail": "User is not verified"},
                    code="authorization",
                )

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomAuthPairTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"detail": "User is not verified"},
                code="authorization",
            )
        validate_data["email"] = self.user.email
        validate_data["id"] = self.user.id
        return validate_data


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    password1 = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError("password is not mach")
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.message)})

        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"detail": "User is not verified"},
                code="authorization",
            )

        return super().validate(attrs)
