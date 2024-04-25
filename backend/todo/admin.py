from django.contrib import admin
from .models import TodoItem, Subtask, TodoGroup

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1

class TodoSubtask(admin.ModelAdmin):
    inlines = [SubtaskInline]


admin.site.register(TodoGroup)
admin.site.register(TodoItem, TodoSubtask)