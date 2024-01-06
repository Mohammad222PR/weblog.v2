from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from rest_framework import generics
from blog.models import *
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..secure import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class BlogListAndCreateView(generics.GenericAPIView):
    serializer_class = BlogSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        blog = Blog.objects.filter(is_public=True)
        serializers = self.serializer_class(instance=blog, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            serializers.validate_data["is_public"] = True
            return Response(
                data={"details": "is created"}, status=status.HTTP_201_CREATED
            )
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailAndUpdateView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadonly,
        IsHaveMembership,
    ]
    parser_classes = (MultiPartParser,)

    # @method_decorator(cache_page(60))
    def get(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        serializers = BlogSerializer(instance=blog)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        serializers = BlogSerializer(instance=blog, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
