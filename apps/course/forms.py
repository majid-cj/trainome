from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


class CourseForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    cover = forms.ImageField()
    price = forms.CharField()
    discount = forms.CharField()
    lectures = forms.CharField()
    trainee = forms.CharField()
    trainee_image = forms.ImageField()

    class Meta:
        model = Course
        fields = [
            'category', 'center', 'name', 'price', 'discount', 'lectures', 'description', 'cover', 'trainee', 'trainee_image'
        ]


class CoursePaymentForm(forms.ModelForm):
    payment = forms.ImageField(label=_("upload payment screenshot"))

    class Meta:
        model = CoursePayment
        fields = [
            'payment',
        ]


class LectureForm(forms.ModelForm):
    name = forms.CharField()
    file = forms.FileField()

    class Meta:
        model = Lecture
        fields = [
            'name', 'file'
        ]
