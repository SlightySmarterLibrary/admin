from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator




class Store(models.Model):
    adult_masks = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    children_masks = models.PositiveIntegerField(validators=[MinValueValidator(0)])