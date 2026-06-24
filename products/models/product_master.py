from django.db import models
from core.constants import Units
from core.models import BaseModel


class ProductMaster(BaseModel):
    name = models.CharField(max_length=250)
    unit = models.CharField(
        max_length=Units.MAX_LENGTH,
        choices=Units.CHOICES,
    )
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

