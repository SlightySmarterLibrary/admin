from django.db import models


class Store(models.Model):
    """
      A store in our system that provides mask.
    """
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=300)
    inventory = {
        "adult": models.IntegerField(),
        "children": models.IntegerField(),
    }
    address = models.CharField(max_length=300)
