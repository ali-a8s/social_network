from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'slug', 'created_at']
    search_fields = ['slug', 'user']
    list_filter = ['updated_at']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['user']
