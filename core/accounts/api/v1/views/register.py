from rest_framework import generics
from ..serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from ..utils import EmailSend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import jwt
from django.conf import settings
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
)

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            email = serializers.validated_data["email"]
            data = {
                "email": email,
            }
            user = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user=user)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailSend(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """
        generate access tokens(JWT) for a given user
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResendActivationTokenView(generics.GenericAPIView):
    serializer_class = ResendActivationCodeSerializers
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            user_obj = serializers.validated_data["user"]
            token = self.get_tokens_for_user(user=user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[user_obj.email],
            )
            EmailSend(email_obj).start()
            return Response(
                {"message": "we are send email for your email"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """
        generate access tokens(JWT) for a given user
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivateVerificationView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")

        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except InvalidSignatureError:
            return Response(
                {"details": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = get_user_model(User, id=user_id)

        if user_obj.is_verified:
            return Response(
                {"details": "user is verified"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "user is verified"}, status=status.HTTP_202_ACCEPTED
        )


