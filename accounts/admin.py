from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_filter = ['created']
    raw_id_fields = ['from_user', 'to_user']



 