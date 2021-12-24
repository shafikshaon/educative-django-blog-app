from django.db import models


class PublishedManager(models.Manager):
    """
    Custom manager
    """
    def published(self):
        return self.get_queryset().filter(status='published')
