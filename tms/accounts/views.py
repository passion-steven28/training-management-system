from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login to continue.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def settings(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:settings')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/settings.html', {'form': form})

class UserListView(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    
    def test_func(self):
        return self.request.user.user_type == 'admin'

class UserDetailView(UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    
    def test_func(self):
        return self.request.user.user_type == 'admin'

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
            
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 'admin':
                return '/dashboard/admin/'
            elif self.request.user.user_type == 'trainer':
                return '/dashboard/trainer/'
            elif self.request.user.user_type == 'participant':
                return '/dashboard/participant/'
        return '/'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    next_page = 'accounts:login'