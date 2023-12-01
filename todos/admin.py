from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'update_at', 'isCompleted', 'deadline')


admin.site.register(Todo, TodoAdmin)
