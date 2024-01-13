import pytest
from django.urls import reverse, resolve
from blog.api.v1.views import *


@pytest.mark.django_db
class TestBlogApiUrl:
    def test_blog_list_url(self):
        url = reverse("blog:api-v1:blog-list")
        assert resolve(url).func.view_class, BlogListAndCreateView

    def test_blog_detail_url(self):
        url = reverse("blog:api-v1:blog-detail-and-update", kwargs={"pk": 57})
        assert resolve(url).func.view_class, BlogDetailAndUpdateView
