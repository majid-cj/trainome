from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import os

from phonenumber_field.modelfields import PhoneNumberField

from apps.common import upload, validate_file

# Create your models here.
class Course(models.Model):
    DRAWING = 1
    PROGRAMMING = 2
    ADOBE = 3
    OPTIONS = (
        (DRAWING, _('Drwaing')),
        (PROGRAMMING, _('Programming')),
        (ADOBE, _('Adobe Package')),
    )
    category = models.IntegerField(choices=OPTIONS)
    center = models.ForeignKey('center.Center', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    cover = models.ImageField(upload_to=upload.wrapper_course_cover)
    price = models.FloatField()
    discount = models.FloatField()
    lectures = models.IntegerField()
    trainee = models.CharField(max_length=250, null=True, blank=True)
    trainee_image = models.ImageField(upload_to=upload.wrapper_trainee_image, null=True, blank=True)
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def get_views(self):
        count = CourseView.objects.filter(course=self).count()
        if count > 1000000:
            count = '{}m'.format(count/1000000)
        elif count > 1000:
            count = '{}k'.format(count/1000)
        else:
            count = '{}'.format(count)
        return count

    def get_rates(self):
        sum_rate = CourseRate.objects.filter(course=self).aggregate(sum=models.Sum('rate'))['sum']
        sum_count = CourseRate.objects.filter(course=self).count()
        sum_rate = sum_rate if sum_rate else 0
        sum_count = sum_count if sum_count != 0 else 1
        return sum_rate/sum_count


class CourseRate(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)
    rate = models.IntegerField()
    add_date = models.DateTimeField(auto_now_add=True)


class CourseComment(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    add_date = models.DateTimeField(auto_now_add=True)


class CoursePayment(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey('accounts.Member', on_delete=models.CASCADE, null=True, blank=True)
    payment = models.ImageField(upload_to=upload.wrapper_payment_screen_shot)
    phone = PhoneNumberField(region='SD')
    allow_access = models.BooleanField(default=False)
    add_date = models.DateTimeField(auto_now_add=True)


class CourseView(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'account']


class Lecture(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    file = models.FileField(
        upload_to=upload.wrapper_lecture_file,
        validators=[validate_file.validate_lecture_extension]
    )
    duration = models.FloatField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.duration} mins"


class LectureAttend(models.Model):
    lecture = models.ForeignKey('course.Lecture', on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['lecture', 'account']

# =================================================================================================

@receiver(models.signals.pre_save, sender=Course)
def auto_delete_course_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).cover
    except sender.DoesNotExist:
        return False

    new_image = instance.cover
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(models.signals.pre_delete, sender=Course)
def auto_delete_course_file_on_delete(sender, instance, **kwargs):
    if not instance.pk:
        return False

    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Lecture)
def auto_delete_lecture_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_image = instance.file
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(models.signals.pre_delete, sender=Lecture)
def auto_delete_lecture_file_on_delete(sender, instance, **kwargs):
    if not instance.pk:
        return False

    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
