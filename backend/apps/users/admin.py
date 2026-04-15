from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User
from apps.consumers.models import ConsumerProfile

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = ConsumerProfile
    can_delete = False
    extra = 0  # no extra forms for profiles
    verbose_name_plural = 'profiles'

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'account_type', 'date_joined', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('account_type','date_joined', 'is_staff','is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    inlines = (ProfileInline,)

