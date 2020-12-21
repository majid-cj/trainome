from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver
import os
from uuid import uuid4

# Create your models here.


def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('menu_logos/', '{}.{}'.format(uuid4().hex, ext))


class HomeMenu(models.Model):
    menu_name = models.CharField(max_length=150)
    menu_url = models.CharField(max_length=250, unique=True)
    menu_priority = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    menu_logo = models.ImageField(upload_to=wrapper)

    def __str__(self):
        return f"{self.menu_name} - {self.menu_url}"


class HomeMenuPermission(models.Model):
    member_type = models.IntegerField()
    menu = models.ForeignKey(HomeMenu, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["member_type", "menu"]



@receiver(models.signals.pre_save, sender=HomeMenu)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).menu_logo
    except sender.DoesNotExist:
        return False

    new_file = instance.menu_logo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.pre_delete, sender=HomeMenu)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if not instance.pk:
        return False

    if os.path.isfile(instance.menu_logo.path):
        os.remove(instance.menu_logo.path)
