from rest_framework import generics
from rest_framework.views import APIView
from accounts.models import *
from accounts.models import Membership
from ..serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(user=self.request.user)
        return obj


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializers(
            instance=profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"details": "your profile update successfully"},
                status=status.HTTP_200_OK,
            )


class MembershipView(generics.GenericAPIView):
    serializer_class = MembershipSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        membership = Membership.objects.get(user=request.user)
        serializers = MembershipSerializer(instance=membership)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            serializers.validated_data["user"] = request.user
            return Response(
                data={"details": "now you have membership"}, status=status.HTTP_200_OK
            )
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
