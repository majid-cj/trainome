from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        return render(
            request, 
            template_name='_home/index.html', 
        )
