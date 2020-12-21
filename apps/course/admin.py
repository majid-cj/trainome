from django.contrib import admin
from .models import (
    Course,
    CourseRate,
    CourseView,
    CourseComment,
    CoursePayment,
    Lecture,
    LectureAttend
)

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseRate)
admin.site.register(CourseView)
admin.site.register(CourseComment)
admin.site.register(CoursePayment)
admin.site.register(Lecture)
admin.site.register(LectureAttend)
