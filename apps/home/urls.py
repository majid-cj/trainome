from django.urls import re_path
from .views import HomeView

app_name = 'home'

urlpatterns = [
    re_path('', HomeView.as_view(), name='index'),
]