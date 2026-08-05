from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Relation


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/user_register.html'

    # blocking logged in users from accessing registration page
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

    # store the 'next' GET parameter for redirection
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

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
                if self.next: # redirct to targer page
                    return redirect(self.next)
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
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, 
                                           to_user=user)
        is_following = relation.exists() # to check if the user already follows this profile to show the Follow/Unfollow button
        return render(request, 'accounts/user_profile.html', {'user': user, 
                                                              'posts': posts,
                                                              'is_following': is_following})


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, f'you already following {user.username}', 'warning')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request,f'you followed {user.username}', 'success')
        return redirect('accounts:user_profile', user.id)


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, f'you unfollowed {user.username}', 'success')
        else:
            messages.error(request, f'you are not following {user.username}', 'warning')
        return redirect('accounts:user_profile', user.id)


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm
    template_name = 'accounts/edit_profile.html'

    def get(self, request):
        form = self.form_class(instance=request.user.profile,
                               initial= {'email':request.user.email})
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST,
                               instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'profile edited successfully.', 'success')
        return redirect('accounts:user_profile', request.user.id)