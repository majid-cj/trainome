from django.urls import re_path
from .views import *

app_name = 'accounts'

urlpatterns = [
    re_path(r'^trend/$', TrendingProfilesListView.as_view(), name='trend'),
    re_path(r'^add/$', AccountCreateView.as_view(), name='add'),
    re_path(r'^edit/(?P<pk>[0-9]+)/$', AccountUpdateView.as_view(), name='edit'),
    re_path(r'^edit/(?P<pk>[0-9]+)/password/$', AccountChangePassword.as_view(), name='edit_password'),
    re_path(r'^delete/(?P<pk>[0-9]+)/$', delete_account, name='delete'),
    re_path('', AccountHomeView.as_view(), name='index'),
]
