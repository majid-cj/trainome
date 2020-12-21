from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView)
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Member
from .forms import (
    MemberForm,
    UserLoginForm,
    EditMemberForm,
    EditPasswordForm)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


# Create your views here.
class UserLogin(View):
    template_name = '_registration/login.html'
    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        form = UserLoginForm(request.POST)
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home:index')
        else:
            form.add_error('email', '')
            form.add_error('password', 'user email or password is wrong')
            return render(request, self.template_name, {'form': form})



@method_decorator(login_required, name='dispatch')
class AccountHomeView(ListView):
    model = Member
    context_object_name = 'members'
    template_name = '_accounts/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Member.objects.all().order_by('-name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_types"] = [{'id': x[0], 'type': x[1]} for x in Member._meta.get_field('member_type').choices]
        return context


@method_decorator(login_required, name='dispatch')
class AccountCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = '_accounts/add_member.html'
    success_url = reverse_lazy('accounts:index')


@method_decorator(login_required, name='dispatch')
class AccountUpdateView(UpdateView):
    model = Member
    context_object_name = 'member'
    form_class = EditMemberForm
    template_name = '_accounts/edit_member.html'
    success_url = reverse_lazy('accounts:index')


@method_decorator(login_required, name='dispatch')
class AccountChangePassword(UpdateView):
    model = Member
    form_class = EditPasswordForm
    template_name = '_accounts/edit_member_password.html'
    success_url = reverse_lazy('accounts:index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.clean_password2():
            self.object.save()
            return super(AccountChangePassword, self).form_valid(form)
        else :
            form.add_error(None, 'enter a valid password')
            return super(AccountChangePassword, self).form_invalid(form)


@login_required
def delete_account(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('accounts:index')
