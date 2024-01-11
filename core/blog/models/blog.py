from django.db import models
from accounts.models import *
from ckeditor.fields import RichTextField
from blog.api.validators import *


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, validators=[validate_tag_title])

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.ForeignKey(User, related_name="blog", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[validate_blog_title])
    body = RichTextField()
    slug = models.SlugField(max_length=30, validators=[validate_blog_slug])
    image = models.ImageField(
        upload_to="images/blog/image", validators=[validate_file_image]
    )
    category = models.ForeignKey(
        Category, related_name="blog", on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(Tag, related_name="blog")
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_public = models.BooleanField(default=False)
    need_membership = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def snipes(self):
        body = self.body[0:10] + "..."
        return body


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=200)
    message = models.TextField(max_length=200)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
