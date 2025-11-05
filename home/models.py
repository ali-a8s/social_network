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
        return f'{self.user} posted {self.title} in {self.created}'

    def get_absolute_url(self):
        return reverse("home:post_detail", args=[self.id, self.slug])
    
    