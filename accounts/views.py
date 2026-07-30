from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/user_register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you cant access this page.', 'warning')
            return redirect('posts:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            User.objects.create_user(username=cd['username'], 
                                     password=cd['password'],
                                     email=cd['email'])
            messages.success(request, 'account created successfully', 'success')
            return redirect('accounts:user_login')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_clas = UserLoginForm
    template_name = 'accounts/user_login.html'

    def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                messages.error(request, 'you cant access this page.', 'warning')
                return redirect('posts:home')
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_clas()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_clas(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('posts:home')
            messages.error(request, 'username/password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect("posts:home")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, 'accounts/user_profile.html', {'user':user, 'posts':posts})