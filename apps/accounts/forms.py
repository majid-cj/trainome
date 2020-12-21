from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
    ReadOnlyPasswordHashField)
from .models import Member


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': _('user email')}), required=True)
    password = ReadOnlyPasswordHashField(
        label='Password', widget=forms.PasswordInput(attrs={'placeholder': _('password')})
    , required=True)

    class Meta:
        model = Member
        fields = [
            'email',
            'password']


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('user first name')}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('user last name')}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': _('user email')}), required=True)
    password1 = ReadOnlyPasswordHashField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": _("enter your password")}), required=True)
    password2 = ReadOnlyPasswordHashField(label='Password confirmation', widget=forms.PasswordInput(
        attrs={"placeholder": _("confirm your password")}), required=True)

    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2']

    def save(self, commit=True):
        user = super(UserSignupForm, self).save(commit=False)
        user.member_type = 3
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class MemberForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('user last name')}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('user last name')}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': _('user email')}))
    password1 = ReadOnlyPasswordHashField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": _("enter your password")}))
    password2 = ReadOnlyPasswordHashField(label='Password confirmation', widget=forms.PasswordInput(
        attrs={"placeholder": _("confirm your password")}))

    class Meta:
        model = Member
        fields = [
            'member_type',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2', ]

    def save(self, commit=True):
        user = super(MemberForm, self).save(commit=False)
        user.is_staff = True if user.member_type in [1, 2] else False
        user.is_superuser = True if user.member_type in [1] else False
        if commit:
            user.save()
        return user


class EditMemberForm(UserChangeForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('user name')}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': _('user email')}))

    class Meta:
        model = Member
        fields = [
            'member_type',
            'name',
            'email']
        exclude = ['password']

    def save(self, commit=True):
        user = super(EditMemberForm, self).save(commit=False)
        user.is_staff = True if user.member_type in [1, 2] else False
        user.is_superuser = True if user.member_type in [1] else False
        if commit:
            user.save()
        return user


class EditPasswordForm(UserChangeForm):
    password1 = ReadOnlyPasswordHashField(widget=forms.PasswordInput(attrs={"placeholder": _("enter your password")}))
    password2 = ReadOnlyPasswordHashField(widget=forms.PasswordInput(attrs={"placeholder": _("confirm your password")}))

    class Meta:
        model = Member
        exclude = ['password', ]
        fields = [
            'password1',
            'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super(EditPasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
