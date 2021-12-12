from django.db import models


class PublishedManager(models.Manager):
    """
    Custom manager
    """

    def get_queryset(self):
        def published(self):
            return self.get_queryset().filter(status='published')
