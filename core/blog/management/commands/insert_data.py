from random import randint

from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Blog
import random
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

category_list = [
    "programing",
    "data science",
]

tag_list = ["js", "python", "java"]


class Command(BaseCommand):
    help = "inserting_data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(),
            username=self.fake.first_name(),
            password="swd2@dwdasdw",
        )

        for title in category_list:
            Category.objects.get_or_create(title=title)

        for title in tag_list:
            Tag.objects.get_or_create(title=title)

        for _ in range(10):
            tag_queryset = list(Tag.objects.all())

            selected_tags = random.sample(tag_queryset, k=randint(1, len(tag_list)))

            blog = Blog.objects.create(
                author=user,
                title=self.fake.paragraph(nb_sentences=4),
                body=self.fake.paragraph(nb_sentences=10),
                slug=self.fake.slug(),
                image=SimpleUploadedFile(
                    "Mohammad_Eslami.png",
                    content=b"file_content",
                    content_type="image/png",
                ),
                category=Category.objects.get(title=random.choice(category_list)),
                created_time=datetime.now(),
                updated_time=datetime.now(),
                is_public=True,
                need_membership=random.choice([True, False]),
            )
            blog.tag.set(selected_tags)
