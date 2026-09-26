from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView
from django.views import View
from .models import Post, Comment, Vote
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm, PostSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class HomeView(View):
        form_class = PostSearchForm

        def get(self, request):
            posts = Post.objects.all()
            
            if request.GET.get('search'): # search in titles and bodies
                  posts = posts.filter(Q(body__icontains=request.GET['search']) | 
                                       Q(title__icontains=request.GET['search']))
            return render(request, 'posts/index.html', {'posts': posts,
                                                        'form':self.form_class()})


class PostDeteilView(View):
      form_class = CommentCreateForm
      form_clas_reply = CommentReplyForm

      def setup(self, request, *args, **kwargs):
          '''
          getting the post
          '''
          self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
          return super().setup(request, *args, **kwargs)

      def get(self, request, *args, **kwargs):
            comments = self.post_instance.pcomment.filter(is_reply=False)
            can_like = False 

            if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
                  can_like = True
            return render(request, 'posts/detail.html', {'post': self.post_instance,
                                                         'comments':comments,
                                                         'form':self.form_class(),
                                                         'reply_form':self.form_clas_reply(),
                                                         'can_like':can_like})

      @method_decorator(login_required)
      def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            
            if form.is_valid():
                  new_comment = form.save(commit=False)
                  new_comment.user = request.user
                  new_comment.post = self.post_instance
                  new_comment.save()
                  messages.success(request, 'comment save successfully', 'success')
                  return redirect("posts:post_detail", self.post_instance.id, self.post_instance.slug)


class PostAddReplyView(LoginRequiredMixin, View):
      form_class = CommentReplyForm

      def post(self, request, post_id, comment_id):
            post = get_object_or_404(Post, id=post_id)
            comment = get_object_or_404(Comment, id=comment_id)
            form = self.form_class(request.POST)

            if form.is_valid():
                  reply = form.save(commit=False)
                  reply.user = request.user
                  reply.post = post
                  reply.reply = comment
                  reply.is_reply = True
                  reply.save()
                  messages.success(request, 'comment save successfully', 'success')
            return redirect("posts:post_detail", post.id, post.slug)

      def options(self, request, *args, **kwargs):
          response = super().options(request, *args, **kwargs)
          response.headers['host'] = 'localhost'
          response.headers['user'] = request.user
          return response

      def http_method_not_allowed(self, request, *args, **kwargs):
            return render(request, 'method_not_allowed.html')


class PostCreateView(LoginRequiredMixin, View):
      form_class = PostCreateUpdateForm
      template_name = 'posts/create.html'

      def get(self, request, *args, **kwargs):
            form = self.form_class()
            return render(request, self.template_name, {'form':form})

      def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)

            if form.is_valid():
                  new_post = form.save(commit=False)
                  new_post.slug = slugify(form.cleaned_data['title'])
                  new_post.user = request.user
                  new_post.save()
                  messages.success(request, 'post deleted successfully', 'success')
                  return redirect('posts:post_detail', new_post.id, new_post.slug)


class PostUpdateView(LoginRequiredMixin, View):
      form_class = PostCreateUpdateForm
      template_name = 'posts/update.html'

      def setup(self, request, *args, **kwargs):
          '''
          getting the post
          '''
          self.post_instance = get_object_or_404(pk= kwargs['post_id'])
          return super().setup(request, *args, **kwargs)

      def dispatch(self, request, *args, **kwargs):
          '''
          check if the user is the onwer of the post
          '''
          post = self.post_instance

          if request.user.id != post.user.id:
                messages.error(request, 'you cant update this post', 'danger')
                return redirect('posts:home')
          return super().dispatch(request, *args, **kwargs)

      def get(self, request, *args, **kwargs):
            post = self.post_instance
            form = self.form_class(instance=post)
            return render(request, self.template_name, {'form':form})

      def post(self, request, *args, **kwargs):
            post = self.post_instance
            form = self.form_class(request.POST, instance=post)

            if form.is_valid():
                  new_post = form.save(commit=False)
                  new_post.slug = slugify(form.cleaned_data['title'])
                  new_post.save()
                  messages.success(request, 'post updated successfully', 'success')
                  return redirect("posts:post_detail", new_post.id, new_post.slug)


class PostDeleteView(LoginRequiredMixin, View):
      def get(self, request, post_id):
            post = get_object_or_404(Post, pk=post_id)

            if request.user.id == post.user.id:
                  post.delete()
                  messages.success(request, 'post deleted successfully', 'success')
            else:
                  messages.error(request, 'you cant delete this post', 'danger')
            return redirect('posts:home')    


class PostLikeView(LoginRequiredMixin, View):
      def get(self, request, post_id):
            post = get_object_or_404(Post, id=post_id)
            like = Vote.objects.filter(user=request.user,
                                       post = post)
            if like.exists():
                  messages.error(request, 'you already liked this post.', 'warning')
            else:
                  Vote.objects.create(user=request.user,
                                      post = post)
                  messages.success(request, 'you liked this post successfully.', 'success')
            return redirect('posts:post_detail', post.id, post.slug)


class AboutView(TemplateView):
      template_name = 'posts/about.html'

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['user'] = self.request.user
            return context


class ContactView(RedirectView):
      pattern_name = 'posts:about'
      permanent = True

      def get_redirect_url(self, *args, **kwargs):
            print('='*90)
            print('proccessing your request...')
            return super().get_redirect_url(*args, **kwargs)