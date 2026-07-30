from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class HomeView(View):
        def get(self, request):
            posts = Post.objects.all()
            return render(request, 'posts/index.html', {'posts': posts})


class PostDeteilView(View):
      def get(self, request, post_id, post_slug):
            post = Post.objects.get(id=post_id, slug=post_slug)
            return render(request, 'posts/detail.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
      def get(self, request, post_id):
            post = Post.objects.get(pk=post_id)
            if request.user.id == post.user.id:
                  post.delete()
                  messages.success(request, 'post deleted successfully', 'success')
            else:
                  messages.error(request, 'you dont have premission to delete this post', 'danger')
            return redirect("posts:home")    