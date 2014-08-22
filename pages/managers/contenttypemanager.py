from django.db import models


class ContentTypeManager(models.Manager):

    def extended(self):
        """Return queryset with only extended content types"""
        return self.get_query_set().filter(is_extended=True)
