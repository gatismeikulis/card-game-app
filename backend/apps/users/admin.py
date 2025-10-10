from django.contrib import admin

from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ["id", "email", "username", "screen_name", "description", "password"]


admin.site.register(User, UserAdmin)
