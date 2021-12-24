from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from blog.models import Post


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker()
        # Create users
        for i in range(20):
            u = User()
            u.email = fake.email()
            u.first_name = fake.first_name()
            u.last_name = fake.last_name()
            u.username = fake.user_name()
            u.set_password('1234')
            u.save()

        # Create blogs
        for i in range(150):
            p = Post()
            p.title = fake.text().split('\n')[0]
            p.body = fake.text()
            p.slug = fake.slug()
            p.author_id = fake.random_int(1, 20)
            p.status = fake.random_element(['draft', 'published'])
            p.created = timezone.now() - timedelta(hours=fake.random_int())
            p.publish = p.created + timedelta(hours=10)
            p.save()
