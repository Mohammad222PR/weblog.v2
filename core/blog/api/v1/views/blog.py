from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from blog.models import *
from ..serializers import *
from ...pagination import PaginationClass
from ..permissions import *
from rest_framework.viewsets import ModelViewSet


class BlogListAndCreateView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser,)
    queryset = Blog.objects.filter(is_public=True)
    pagination_class = PaginationClass
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "category",
        "is_public",
        "need_membership",
        "tag",
    ]
    search_fields = [
        "title",
    ]
    ordering_fields = [
        "created_time",
        "updated_time",
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, is_public=True)


class BlogDetailAndUpdateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]
    parser_classes = (MultiPartParser,)
    serializer_class = BlogSerializer

    @method_decorator(cache_page(60))
    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        if (
                blog.need_membership
                and not Membership.objects.filter(user=request.user).exists()
        ):
            return Response(
                {"detail": "This post requires membership, but you don't have it"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BlogSerializer(instance=blog, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(instance=blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        blog.delete()
        return Response(
            data={"success": "Your blog was deleted successfully"},
            status=status.HTTP_202_ACCEPTED
        )


class TagView(APIView):
    serializer_class = PostTagSerializers
    parser_classes = (MultiPartParser,)
    pagination_class = PaginationClass

    def get(self, request, pk):
        tag = Tag.objects.get(id=pk)
        result = tag.blog.all()
        serializer = PostTagSerializers(instance=result, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryView(APIView):
    serializer_class = PostCategorySerializers
    parser_classes = (MultiPartParser,)
    pagination_class = PaginationClass

    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        result = category.blog.all()
        serializer = PostTagSerializers(instance=result, many=True, context={'request': request})
        return Response(serializer.data)

# class CommentView(ModelViewSet):
#     serializer_class = CommentSerializer
#     parser_classes = (MultiPartParser,)
#     permission_classes = [IsAuthenticated, IsCommentOwner]
#
#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             user_comment = Comment.objects.filter(user=self.request.user)
#             return user_comment
#         else:
#             return Comment.objects.none()
