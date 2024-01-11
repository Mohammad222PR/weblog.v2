import pytest
from datetime import datetime
from accounts.models import User
from ..models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError


@pytest.fixture
def user():
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


@pytest.mark.django_db
class TestModel_Blog_Tag_Category_Comment:

    """Test blog model"""

    def test_blog_model_vaild_data(self, image, category, tag, user):
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

        # Asserts for basic model existence
        assert Blog.objects.filter(pk=blog.id).exists()

    def test_blog_model_invalid_data(self):
        with pytest.raises(Exception):
            Blog.objects.create()

    """test tag"""

    def test_tag_valid_data(self):
        tag = Tag.objects.create(title="test tag title")

        assert Tag.objects.filter(title=tag.title).exists()

    def test_tag_invalid_data(self):
        with pytest.raises(IntegrityError):
            Tag.objects.create(
                title=None,
            )

    """test category"""

    def test_category_valid_data(self):
        category = Category.objects.create(title="test category title")

        assert Category.objects.filter(title=category.title).exists()

    def test_category_invalid_data(self):
        with pytest.raises(IntegrityError):
            Category.objects.create(
                title=None,
            )

    """test comment"""

    def test_comment_vaild_data_parent_none_is_publick_true(self, blog, user):
        comment = Comment.objects.create(
            user=user,
            blog=blog,
            title="test comment test",
            message="test comment test message",
            parent=None,
            created_time=datetime.now(),
            is_public=True,
        )

        assert Comment.objects.filter(pk=comment.id).exists()

    def test_comment_vaild_data_parent_is_publick_true(self, blog, user, comment):
        comment = Comment.objects.create(
            user=user,
            blog=blog,
            title="test comment test",
            message="test comment test message",
            parent=comment,
            created_time=datetime.now(),
            is_public=True,
        )

        assert Comment.objects.filter(pk=comment.id).exists()

    def test_comment_vaild_data_parent_is_publick_false(self, blog, user, comment):
        comment = Comment.objects.create(
            user=user,
            blog=blog,
            title="test comment test",
            message="test comment test message",
            parent=comment,
            created_time=datetime.now(),
            is_public=False,
        )

        assert Comment.objects.filter(pk=comment.id).exists()

    def test_comment_vaild_data_parent_none_is_publick_false(self, blog, user, comment):
        comment = Comment.objects.create(
            user=user,
            blog=blog,
            title="test comment test",
            message="test comment test message",
            parent=None,
            created_time=datetime.now(),
            is_public=False,
        )

        assert Comment.objects.filter(pk=comment.id).exists()

    def test_comment_invaild_data(self, blog, user, comment):
        with pytest.raises(Exception):
            Comment.objects.create(
                user="dwa",
            )
