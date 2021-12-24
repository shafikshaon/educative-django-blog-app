from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from blog.models import Post


class Command(BaseCommand):
    help = 'Generate random blogs'
    missing_args_message = 'The total argument must be provided.'
    output_transaction = True
    requires_migrations_checks = False
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of blogs to be created')
        parser.add_argument('-p', '--prefix', type=str, help='Define a blog title prefix', )
        parser.add_argument('-pub', '--published', action='store_true', help='Set published status for the blogs')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        prefix = kwargs['prefix']
        published = kwargs['published']

        for i in range(total):
            p = Post()
            if prefix:
                p.title = prefix + ": " + fake.text().split('\n')[0]
            else:
                p.title = fake.text().split('\n')[0]
            p.body = fake.text()
            p.slug = fake.slug()
            p.author_id = fake.random_int(1, 20)
            if published:
                p.status = 'published'
            else:
                p.status = fake.random_element(['draft', 'published'])
            p.created = timezone.now() - timedelta(hours=fake.random_int())
            p.publish = p.created + timedelta(hours=10)
            p.save()

        self.stdout.write(self.style.SUCCESS('Blogs generated.'))
