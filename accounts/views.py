from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from .models import Relation
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you cant access this page', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], 
                                     email=cd['email'],
                                     password=cd['password1'])
            messages.success(request, 'you registered successfully.', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you cant access this page', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you have logged in', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'username or password is wrong.', 'waening')
        return render(request, self.template_name, {'form':form})
    

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you have logged out', 'success')
        return redirect('home:home')
    

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        is_following = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'accounts/profile.html', {'user':user, 'posts':posts, 'is_following':is_following})
    

class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=target_user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=target_user)
            messages.success(request, 'you followed this user', 'success')
        return redirect('accounts:user_profile', target_user.id)


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=target_user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('accounts:user_profile', target_user.id)
    

class UserFeedView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        following_users = User.objects.filter(id__in=Relation.objects.filter(from_user=user).values('to_user'))
        posts = Post.objects.filter(user__in=following_users).order_by('-updated')
        return render(request, 'accounts/feed.html', {'posts': posts, 'following_users': following_users})
     

class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email':request.user.email})
        return render(request, 'accounts/edit_user.html', {'form':form})    
    
    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile, initial={'email':request.user.email})
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'profile updated successfully', 'success')
        return redirect('accounts:user_profile', request.user.id)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'