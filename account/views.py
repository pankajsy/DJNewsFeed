import base64
import io, boto3, pandas, json, uuid
from django.shortcuts import render
from django.views.decorators.debug import sensitive_variables
from django.views.generic import TemplateView, CreateView, ListView
from PIL import Image
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from datetime import datetime, timedelta
import datetime as dt
from dateutil.relativedelta import relativedelta
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, ModelFormMixin, DeleteView
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
import csv, requests
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

timeformat = '%Y-%m-%d %H:%M:%S'
def index(request):
    if request.user.is_authenticated():
        # return HttpResponseRedirect(reverse('account:admin_users_list'))
        return HttpResponseRedirect(reverse('core:feed'))
    else:
        return HttpResponseRedirect(reverse('account:admin_login'))

class LoginView(CreateView):
    form_class = CleanLoginForm
    template_name = 'account/auth.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, {'form': self.form_class})

    @sensitive_variables('password')
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        messages.get_messages(request)
        if form.is_valid():
            formdata = form.cleaned_data
            email = formdata['email']
            password = formdata['password']
            user = self.authenticate_via_email(email, password)
            if not user:
                messages.error(request, "Sorry, Invalid Credentials. Please try again.")
            else:
                # if user.is_staff:
                user = authenticate(username=user.username, password=password)
                if user:
                    login(self.request, user)
                    return HttpResponseRedirect(reverse('account:admin_index'))
                else:
                    messages.error(request, "Sorry, No admin privileges granted!")

        return render(request, self.template_name, {'form': self.form_class})

    def authenticate_via_email(self, email, password):
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                if user.check_password(password):
                    return user
            except ObjectDoesNotExist:
                pass
        return None

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('account:admin_login'))

class RegisterUser(CreateView):
    form_class = UserForm
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, {'form': self.form_class})

    @sensitive_variables('password', 'confirm_password')
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        messages.get_messages(request)
        try:
            if form.is_valid():
                formdata = form.cleaned_data
                email = formdata['email']
                username = email
                password = formdata['password']
                confirm_password = formdata['confirm_password']
                if confirm_password == password:
                    user = User.objects.create_user(email = email,
                                               username = username,
                                               password = password)
                    user.first_name = formdata['first_name']
                    user.last_name = formdata['last_name']
                    user.save()

                    if not user:
                        messages.error(request, "Sorry, something went wrong, please try again.")
                    else:
                        up, created = Userprofile.objects.get_or_create(user = user)
                        uuid_str = str(uuid.uuid5(uuid.NAMESPACE_URL, email.encode('utf-8')))
                        up.uuid = uuid_str
                        up.save()

                        user = authenticate(username=user.username, password=password)
                        if user:
                            login(self.request, user)
                            return HttpResponseRedirect(reverse('account:admin_index'))
                        else:
                            messages.error(request, "Sorry, something went wrong, please try again.")
                else:
                    messages.error(request, "Sorry, both passwords mismatch")

            else:
                for e in form.errors.as_data():
                    messages.error(request, form.errors[e])

        except Exception as e:
            print(e.message)
            messages.error(request, e.message)

        return render(request, self.template_name, {'form': self.form_class})

class AddNewUser(LoginRequiredMixin, FormView):
    form_class = NewUserForm
    template_name = 'account/addnewuser.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        title = "Add New User"
        return render(request, self.template_name, {'form': form, 'title':title})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            non_existing_email = User.objects.filter(email=formdata['email']).count() == 0
            if non_existing_email:
                u = User.objects.create(username = formdata['email'],
                                        email = formdata['email'],
                                        first_name = formdata['first_name'],
                                        last_name = formdata['last_name'])
                u.set_password(formdata['password'])
                u.save()
                tokens = Token.objects.filter(user=u)
                for i in tokens:
                    i.delete()
                token = Token.objects.create(user=u)
                messages.success(request, {"email": u.email, "status": "success", "token": token.key})
            else:
                messages.error(request, {"email": form.cleaned_data['email'], "status": "error", "error": "User with that email already exist!"})
        else:
            print (form.errors)
        return render(request, self.template_name, {'form': form})


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    # success_url = reverse_lazy('account:admin_users_list')
    # fields = ['first_name', 'last_name', 'email']
    template_name = 'account/user_update_form.html'
    form_class = UserProfileSaveForm
    # def form_valid(self, form):
    #     form.instance.username = form.cleaned_data['email']
    #     self.object = form.save(instance = form.instance)
    #     # self.object.username = form.cleaned_data['email']
    #     return super(UserUpdate, self).form_valid(form)
    #     # return HttpResponseRedirect(self.get_success_url())
    #
    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def get_object(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return user
    #
    def get_success_url(self):
        return reverse('account:admin_index')

class ListUsers(LoginRequiredMixin, TemplateView):
    template_name = "account/userslist.html"
    title = "List of Users"
    login_url = 'account:admin_login'

    def get_context_data(self, **kwargs):
        context = super(ListUsers, self).get_context_data(**kwargs)
        users = Userprofile.objects.all()
        if users.count() > 0:
            paginator = Paginator(users, 20)
            page = self.request.GET.get('userspage')
            try:
                final_users = paginator.page(page) #
            except PageNotAnInteger:
                final_users = paginator.page(1)
            except EmptyPage:
                final_users = paginator.page(paginator.num_pages)
            context['users'] = final_users
        return context


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/user_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'users'  # Default: object_list
    paginate_by = 10
    queryset = Userprofile.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UserListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['admin'] = self.request.user.is_staff
        return context

class UserDelete(LoginRequiredMixin, View):
    # login_url = "account:admin_login"
    def post(self, request, format=None):
        if User.objects.filter(pk=int(request.POST['pk'])).count() > 0:
            User.objects.filter(pk=int(request.POST['pk']))[0].delete()
        return HttpResponseRedirect(reverse('account:admin_users_list'))
