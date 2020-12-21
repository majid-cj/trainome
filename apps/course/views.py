from django.views.generic import (
    ListView,
    CreateView,
    DetailView
    UpdateView
)
from django.views import View
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .models import (
    Course,
    CourseView,
    Lecture
)
from apps.center.models import Center
from .forms import *

# Create your views here.

@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = '_course/index.html'
    paginate_by = 8

    def get_queryset(self):
        return Course.objects.all().order_by('-name')


@method_decorator(login_required, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = '_course/add.html'
    success_url = reverse_lazy("course:index")

    def get_context_data(self, **kwargs):
        kwargs['centers'] = Center.objects.all().order_by('name')
        return super(CourseCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            self.object.save()
            return super(CourseCreateView, self).form_valid(form)
        else:
            form.add_error(None, _('error occured !'))
            return super(CourseCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = '_course/detail.html'


@method_decorator(login_required, name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    context_object_name = 'course'
    template_name = '_course/update.html'
    success_url = reverse_lazy("course:index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            self.object.save()
            return super(CourseUpdateView, self).form_valid(form)
        else:
            form.add_error(None, _('error occured !'))
            return super(CourseUpdateView, self).form_valid(form)


@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect(reverse("course:index"))


@method_decorator(login_required, name='dispatch')
class LectureListView(ListView):
    model = Lecture
    context_object_name = 'lectures'
    template_name = '_course/_lecture/index.html'
    paginate_by = 8

    def get_queryset(self):
        return Lecture.objects.all().order_by('-name')


@method_decorator(login_required, name='dispatch')
class LectureCreateView(CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = '_course/_lecture/add.html'
    success_url = reverse_lazy("lecture:index")

    def get_context_data(self, **kwargs):
        kwargs['categories'] = LectureCategory.objects.all().order_by('name')
        kwargs['centers'] = Center.objects.all().order_by('name')
        return super(LectureCategoryCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            self.object.save()
            return super(LectureCreateView, self).form_valid(form)
        else:
            form.add_error(None, _('error occured !'))
            return super(LectureCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class LectureDetailView(DetailView):
    model = Lecture
    context_object_name = 'lecture'
    template_name = '_course/_lecture/detail.html'


@method_decorator(login_required, name='dispatch')
class LectureUpdateView(UpdateView):
    model = Lecture
    form_class = LectureForm
    context_object_name = 'lecture'
    template_name = '_course/_lecture/update.html'
    success_url = reverse_lazy("lecture:index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            self.object.save()
            return super(LectureUpdateView, self).form_valid(form)
        else:
            form.add_error(None, _('error occured !'))
            return super(LectureUpdateView, self).form_valid(form)


@login_required
def delete_course(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    lecture.delete()
    return redirect(reverse("course:index"))
