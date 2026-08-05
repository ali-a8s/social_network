from django.contrib import admin
from .models import Post, Comment, Vote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'slug', 'created_at']
    search_fields = ['slug', 'user']
    list_filter = ['updated_at']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'is_reply', 'created_at']
    raw_id_fields = ['user', 'post', 'reply']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'post']