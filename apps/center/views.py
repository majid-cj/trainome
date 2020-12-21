from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView
)
from django.views import View
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .models import Center
from .forms import CenterForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CenterListView(ListView):
    model = Center
    context_object_name = 'centers'
    template_name = "_center/index.html"
    paginate_by = 8

    def get_queryset(self):
        return Center.objects.all().order_by('-add_date')


@method_decorator(login_required, name='dispatch')
class CenterCreateView(CreateView):
    model = Center
    form_class = CenterForm
    template_name = "_center/add.html"

    def get_success_url(self):
        return reverse("center:index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            self.object.save()
            return super(CenterCreateView, self).form_valid(form)
        else:
            form.add_error(None, _('error occured !'))
            return super(CenterCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CenterDetailView(DetailView):
    model = Center
    context_object_name = 'center'
    template_name = "_center/detail.html"


@method_decorator(login_required, name='dispatch')
class CenterUpdateView(UpdateView):
    model = Center
    form_class = CenterForm
    context_object_name = 'center'
    template_name = "_center/update.html"

    def get_success_url(self):
        return reverse("center:detail", kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.is_valid():
            self.object.save()
            return super(CenterUpdateView, self).form_valid(form)
        else:
            form.add_error(None, _('error occured !'))
            return super(CenterUpdateView, self).form_valid(form)


@login_required
def CenterDeleteView(request, pk):
    center = get_object_or_404(Center, pk=pk)
    center.delete()
    return redirect(reverse("center:index"))
