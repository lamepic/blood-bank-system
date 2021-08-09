from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserProfile, StaffProfile
from .forms import UserForm

# Register your models here.
User = get_user_model()

class InlineUserProfile(admin.StackedInline):
    model = UserProfile

class InlineStaffProfile(admin.StackedInline):
    model = StaffProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [InlineUserProfile, InlineStaffProfile]
    list_display = ['first_name', 'last_name', 'username', 'email']
    form = UserForm
    fields = [
        'first_name', 
        'last_name', 
        'username', 
        'email', 
        'password1', 
        'password2', 
        'is_normalUser', 
        'is_staffUser'
    ]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'gender', 'address', 'blood_group', 'age', 'phone')


    def username(self, obj):
        return f'{obj.user.username}'

@admin.register(StaffProfile)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['fullname']

    def fullname(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    