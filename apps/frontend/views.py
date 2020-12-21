from django.contrib.auth import authenticate, login
from django.views.generic import ListView, CreateView
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy

from rest_framework.authtoken.models import Token

from apps.accounts.models import Member
from apps.accounts.forms import UserSignupForm, UserLoginForm
from apps.course.models import *
from apps.course.forms import *

# Create your views here.

class SigninView(View):
    template_name = '_frontend/_registration/signin.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return redirect('frontend:index')
            else:
                form.add_error('password', 'user email or password is wrong')
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class SignupView(View):
    template_name = '_frontend/_registration/signup.html'
    
    def get(self, request):
        form = UserSignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontend:signin')
        else:
            return render(request, self.template_name, {'form': form})


def HomePage(request):
    return render(request, '_frontend/index.html')


@method_decorator(login_required, name='dispatch')
class UserCourseDetailView(ListView):
    model = Lecture
    paginate_by = 15
    context_object_name = 'lectures'
    template_name = '_frontend/_course/detail.html'

    def get_queryset(self):
        access = CoursePayment.objects.filter(
            course=self.kwargs['pk'], account=self.request.user, allow_access=True
        )
        if access:
            return Lecture.objects.filter(course__pk=self.kwargs['pk']).order_by('pk')
        else:
            return Lecture.objects.filter(course__pk=self.kwargs['pk']).order_by('pk')[:1]

    def get_context_data(self, **kwargs):
        course = Course.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        payment = CoursePayment.objects.filter(course=course, account=user)
        CourseView.objects.get_or_create(course=course, account=self.request.user)
        kwargs["course"] = course
        kwargs["payment"] = True if payment else False
        kwargs["attend"] = LectureAttend.objects.filter(lecture__course=course, account=self.request.user).count()
        return super(UserCourseDetailView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class PayCourseView(CreateView):
    model = CoursePayment
    form_class = CoursePaymentForm
    template_name = '_frontend/_course/payment.html'

    def get_success_url(self):
        return reverse('frontend:course', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            self.object.course = Course.objects.get(pk=self.kwargs['pk'])
            self.object.account = self.request.user
            self.object.save()
            return super(PayCourseView, self).form_valid(form)
        else:
            return super(PayCourseView, self).form_invalid(form)


@login_required
def UserCoursesView(request):
    return render(request, '_frontend/_user_course/index.html')
