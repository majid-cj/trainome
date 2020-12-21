from django.urls import re_path
from django.contrib.auth import views as auth_views
from .views import *


app_name = 'frontend'

urlpatterns = [
    re_path(r'signin/', SigninView.as_view(), name='signin'),
    re_path(r'signup/', SignupView.as_view(), name='signup'),
    re_path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^course/(?P<pk>[0-9]+)/$', UserCourseDetailView.as_view(), name='course'),
    re_path(r'^course/(?P<pk>[0-9]+)/payment/$', PayCourseView.as_view(), name='payment'),
    re_path(r'^account/courses/$', UserCoursesView, name='courses'),
    re_path(r'^$', HomePage, name='index'),
]
