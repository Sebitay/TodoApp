"""
URL configuration for todoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo.views import TodoItemListView, TodoItemDetailView, TodoGroupListView, TodoGroupDetailView, TodoGroupFilterView ,TodoGroupActionView, TodoItemFilterView, TodoItemActionView, TodoSubtaskActionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todos/', TodoItemListView.as_view(), name='todo-list'),
    path('todos/<int:id>/', TodoItemDetailView.as_view(), name='todo-detail'),
    path('todos/filter/', TodoItemFilterView.as_view(), name='todo-filter'),
    path('todos/<int:id>/action/', TodoItemActionView.as_view(), name='todo-action'),
    path('subtask/<int:id>/', TodoSubtaskActionView.as_view(), name='subtask-action'),
    path('groups/', TodoGroupListView.as_view(), name='group-list'),
    path('groups/<int:id>/', TodoGroupDetailView.as_view(), name='group-detail'),
    path('groups/filter/', TodoGroupFilterView.as_view(), name='group-filter'),
    path('groups/<int:id>/action/', TodoGroupActionView.as_view(), name='group-action'),
]
