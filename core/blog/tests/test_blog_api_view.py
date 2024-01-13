import pytest
from datetime import datetime
from accounts.models import User
from blog.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def comment_user():
    user = User.objects.create_user(
        email="admin@example.com", username="admin", password="dad12313"
    )
    return user


@pytest.fixture
def tag():
    tag = Tag.objects.create(title="test_tag")
    return tag


@pytest.fixture
def category():
    cat = Category.objects.create(title="test_category")
    return cat


@pytest.fixture
def image():
    image = SimpleUploadedFile(
        "Mohammad_Eslami.png", content=b"file_content", content_type="image/png"
    )
    return image


@pytest.fixture
def blog(user, tag, category, image):
    blog = Blog.objects.create(
        author=user,
        title="test title",
        body="test body blog",
        slug="test_title",
        image=image,
        category=category,
        created_time=datetime.now(),
        updated_time=datetime.now(),
        is_public=True,
        need_membership=False,
    )
    blog.tag.set([tag])
    return blog


@pytest.fixture
def comment(blog, user):
    comment = Comment.objects.create(
        user=user,
        blog=blog,
        title="test comment test",
        message="test comment test message",
        parent=None,
        created_time=datetime.now(),
        is_public=True,
    )
    return comment


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestBlogView:
    """test blog views"""

    def test_blog_view_status_200(self, api_client, comment_user):
        url = reverse("blog:api-v1:blog-list")
        api_client.force_login(user=comment_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_blog_view_response_401(self, api_client):
        url = reverse("blog:api-v1:blog-list")
        with pytest.raises(Exception):
            response = api_client.get(url)
            assert response.status_code == 401

    def test_blog_view_post_status_200(
        self, api_client, comment_user, image, category, tag
    ):
        url = reverse("blog:api-v1:blog-list")
        data = {
            "author": comment_user,
            "title": "test title",
            "body": "test body",
            "slug": "test-body",
            "image": image,
            "category": category,
            "tag": [tag],
            "created_time": datetime.now(),
            "updated_time": datetime.now(),
            "is_public": True,
            "need_membership": True,
        }
        user = comment_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_blog_view_invalid_user_post_status_200(
        self, api_client, comment_user, image, category, tag
    ):
        url = reverse("blog:api-v1:blog-list")
        data = {
            "author": comment_user,
            "title": "test title",
            "body": "test body",
            "slug": "test-body",
            "image": image,
            "category": category,
            "tag": [tag],
            "created_time": datetime.now(),
            "updated_time": datetime.now(),
            "is_public": True,
            "need_membership": True,
        }
        with pytest.raises(Exception):
            response = api_client.post(url, data)
            assert response.status_code == 400

    def test_blog_view_invalid_data_post_status_200(
        self, api_client, comment_user, image, category, tag
    ):
        url = reverse("blog:api-v1:blog-list")
        data = {}
        user = comment_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_blog_view_invalid_data_and_user_post_status_200(
        self, api_client, comment_user, image, category, tag
    ):
        url = reverse("blog:api-v1:blog-list")
        data = {}
        with pytest.raises(Exception):
            response = api_client.post(url, data)
            assert response.status_code == 401
