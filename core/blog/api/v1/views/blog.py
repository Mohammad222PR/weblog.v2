from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from core.blog.models import *
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..secure import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from core.blog.api.pagination import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BlogListAndCreateView(APIView):
    pagination_class = PaginationBlog
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "tag", "is_public", "need_membership"]
    search_fields = ["title"]

    @method_decorator(cache_page(60))
    def get(self, request):
        blog = Blog.objects.filter(is_public=True)
        serializers = BlogSerializer(
            instance=blog, many=True, context={"request": request}
        )
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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]
    parser_classes = (MultiPartParser,)

    @method_decorator(cache_page(60))
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        if blog.need_membership == True:
            if Membership.objects.filter(user=request.user).exists():
                serializers = BlogSerializer(
                    instance=blog, context={"request": request}
                )
                return Response(data=serializers.data, status=status.HTTP_200_OK)

            else:
                return Response(
                    {"detail": "this post need member ship but you dont have it"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            serializers = BlogSerializer(instance=blog, context={"request": request})
            return Response(data=serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        blog = Blog.objects.get(id=pk)
        serializers = BlogSerializer(instance=blog, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(
                data={"detail": "Comment added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            blog = Blog.objects.get(id=pk)
            blog.delete()
            return Response(
                data={"success": "your blog delete successfully"},
                status=status.HTTP_202_ACCEPTED,
            )
        except blog.DoesNotExist:
            return Response(
                data={"fail": "user does not exist!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
