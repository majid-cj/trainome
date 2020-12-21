from django.urls import re_path
from .views import *
from .views_admin import *

app_name = 'api'


urlpatterns = [
    # Admin 
    # TODO : add admin APIs endpoints

    # Account
    re_path(r'^signin/$', SigninAPI),
    re_path(r'^signup/$', SignupAPI),
    re_path(r'^password/update/$', UpdatePassWordAPI.as_view()),
    re_path(r'^password/reset/$', ResetPasswordAPI.as_view()),
    re_path(r'^course/category/$', CategoryAPI),
    re_path(r'^course/list/$', ListCourseAPI.as_view()),
    re_path(r'^center/list/$', ListTrainingCentersAPI.as_view()),
    re_path(r'^course/(?P<pk>[0-9]+)/category/$', ListCourseByCategoryAPI.as_view()),
    re_path(r'^course/search/$', SearchCourseAPI.as_view()),
    re_path(r'^course/(?P<pk>[0-9]+)/payment/$', CoursePaymentAPI),
    re_path(r'^course/(?P<pk>[0-9]+)/lectures/lecture/$', LectureAPI),
    re_path(r'^course/(?P<pk>[0-9]+)/lectures/$', LecturesAPI.as_view()),
    re_path(r'^course/(?P<pk>[0-9]+)/lectures/(?P<apk>[0-9]+)/attend/$', LecturesAttendAPI),
    re_path(r'^course/(?P<pk>[0-9]+)/comment/$', CourseCommentsAPI.as_view(
        {
            'get': 'list',
            'post': 'create',
            'put': 'update',
            'delete': 'destroy',
        }
    )),
    re_path(r'^course/rate/$', RateCourseAPI),
    re_path(r'^course/access/$', AccessedCoursesAPI.as_view()),
    re_path(r'^course/request/$', RequestedCoursesAPI.as_view()),
    re_path(r'^course/access/search/$', SearchAccessedCoursesAPI.as_view()),
    re_path(r'^course/request/search/$', SearchRequestedCoursesAPI.as_view()),

]
