from django.contrib import admin
from .models import Post, Comment, Vote

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'updated']
    search_fields = ['body', 'title']
    list_filter = ['updated']
    prepopulated_fields = {'slug': ['body']}
    raw_id_fields = ['user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created']
    search_fields = ['user']
    raw_id_fields = ['user', 'post']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'post']
