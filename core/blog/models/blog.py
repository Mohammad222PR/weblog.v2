from django.db import models
from django.contrib.auth import get_user_model
from blog.validators import *
from ckeditor.fields import RichTextField 

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, validators=[validate_tag_title])

    def __str__(self) -> str:
        return self.title


class Blog(models.Model):
    author = models.ForeignKey(User, related_name="blog", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[validate_blog_title])
    body = RichTextField()
    slug = models.SlugField(max_length=30, validators=[validate_blog_slug])
    image = models.ImageField(
        upload_to="images/blog/image", validators=[validate_file_image]
    )
    category = models.ForeignKey(Category, related_name="blog", on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, related_name="blog")

