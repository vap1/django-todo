from django.contrib import admin
from .models import Todo, CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'update_at', 'isCompleted', 'deadline')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(Todo, TodoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)