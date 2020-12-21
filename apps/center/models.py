from django.db import models
from uuid import uuid4
import os

from apps.common.upload import wrapper_center_logo

# Create your models here.

class Center(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    map_location = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to=wrapper_center_logo)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
