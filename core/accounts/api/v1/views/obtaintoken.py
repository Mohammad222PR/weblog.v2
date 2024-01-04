from rest_framework import generics
from ..serializers import *
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class ObtainTokenView(generics.GenericAPIView):
    serializer_class = CustomAuthTokenSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data["user"]
        token, create = Token.objects.get_or_create(user=user)
        return Response(
            data={
                "token": token.key,
                "user": user.username,
                "email": user.email,
            }
        )


class ObtainPairTokenView(TokenObtainPairView):
    serializer_class = CustomAuthPairTokenSerializer
    pagination_class = (MultiPartParser,)


class CustomDiscardAuthView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        request.user.auth_token.delete()
        return Response(
            {"detail": "your token delete successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


