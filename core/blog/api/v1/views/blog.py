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
from blog.api.pagination import Pagination


class BlogListAndCreateView(APIView):
    pagination_class = Pagination
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser,)
    
    def get(self, request):
        blog = Blog.objects.filter(is_public=True)
        serializers = BlogSerializer(instance=blog, many=True, context={'request':request})
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.validated_data["author"] = request.user
            serializers.validated_data["is_public"] = True
            serializers.save()
            return Response(
                data={"details": "is created"}, status=status.HTTP_201_CREATED
            )
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class BlogDetailAndUpdateView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadonly,
    ]
    parser_classes = (MultiPartParser,)

    # @method_decorator(cache_page(60))
    def get(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        serializers = BlogSerializer(instance=blog)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        serializers = BlogSerializer(instance=blog, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, slug):
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data={'detail':'Comment added successfully'}, status=status.HTTP_201_CREATED)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)