from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommenCreateForm, PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


# Create your views here.
class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        form = self.form_class()
        if request.GET.get('search'):
            posts = Post.objects.filter(Q(body__contains=request.GET['search']) | Q(title__contains=request.GET['search']))
        return render(request, 'home/home.html', {'posts': posts, 'form': form})



class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})
 
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'you created a new post', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)



class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk= kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user.id != request.user.id:
            messages.error(request, 'you cant update this post', danger)
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, post_id):
        post = self.post_instance
        form = self.form_class(instance= post)
        return render(request, 'home/update.html', {'form': form})
    
    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'post updated successfully', 'success')
            return redirect('home:post_detail', post.id, post.slug)           



class PostDetailView(View):
    form_class = CommenCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomment.all()
        form = self.form_class()
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'home/detail.html', {'post':self.post_instance, 
        'comments': comments, 
        'form': form, 
        'can_like': can_like
        })
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)



class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted succussfully', 'success')
        else: 
            messages.error(request, 'you cant delete this post', 'danger')
        return redirect('home:home')



class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'you already liked this post', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'you liked this post successfully', 'success')
        return redirect('home:post_detail', post.id, post.slug)
