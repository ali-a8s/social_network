from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user')
    title = models.CharField()
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering= ['-updated']

    def __str__(self):
        return f'{self.user} posted {self.title}'

    def get_absolute_url(self):
        return reverse("home:post_detail", args=[self.id, self.slug])

    def likes_count(self):
        return self.pvote.count()

    def user_can_like(self, user):
        user_like = user.uvote.filter(post=self)
        if user_like.exists():
            return True
        return False



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment') 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'pcomment') 
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.post}"



class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvote') 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'pvote') 

    def __str__(self):
        return f"{self.user} liked {self.post}"
    

       
    