from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from .models import Userprofile


class CleanLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if not User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
    #         raise forms.ValidationError(u'Username "%s" is already in use.' % username)
    #     return username

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(u'Email "%s" is already in use.' % email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 3:
                raise ValidationError("password length too small (min 3 chars)")
            return password
        else:
            raise ValidationError("Couldn't get the password")

class NewUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 3:
                raise ValidationError("password length too small (min 3 chars)")
            return password
        else:
            raise ValidationError("Couldn't get the password")
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')


class UserProfileSaveForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def save(self, user=None):
        userobject = super(UserProfileSaveForm, self).save(commit=False)
        if user:
            print ("Instance")
        userobject.username = userobject.email
        userobject.save()
        return userobject