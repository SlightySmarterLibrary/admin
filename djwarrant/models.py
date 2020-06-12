from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class Store(models.Model):
    adult_masks = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    children_masks = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])


class User(AbstractUser):
    id = models.UUIDField(unique=True, primary_key=True)
    objects = UserManager()
