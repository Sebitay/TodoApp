import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from django.db.models import Q

from .models import TodoItem, TodoGroup, Subtask
from .services import TodoItemService, TodoGroupService, SubtaskService
from .serializers import TodoInputSerializer, TodoOutputSerializer, GroupInputSerializer, GroupOutputSerializer, SubtaskInputSerializer

class TodoItemListView(APIView):
    def get(self, request):
        todo_items = TodoItem.objects.all()
        serializer = TodoOutputSerializer(todo_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoInputSerializer(data=request.data)
        if serializer.is_valid():
            TodoItemService.create(**serializer.validated_data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TodoItemFilterView(APIView):
    def get(self, request):
        delta = request.data.get('date', None)
        group = request.data.get('group', None)
        checked = True if request.data.get('checked', None) == '1' else False

        todos = TodoItem.objects.all()

        if delta is not None:
            day = datetime.date.today() + datetime.timedelta(days=int(delta))
            todos = todos.filter(Q(date=day))
        if group is not None:
            todos = todos.filter(Q(group=group))
        if checked is not None:
            todos = todos.filter(Q(checked=checked))

        serializer = TodoOutputSerializer(todos, many=True)
        return Response(serializer.data)
    
class TodoItemDetailView(APIView):
    def get(self, request, id):
        todo_item = TodoItem.objects.get(id=id)
        serializer = TodoOutputSerializer(todo_item)
        return Response(serializer.data)
    
    def post(self, request, id):
        todo_item = TodoItem.objects.get(id=id)
        serializer = SubtaskInputSerializer(data=request.data)
        if serializer.is_valid():
            content = request.data['content']
            TodoItemService.add_subtask(todo_item, content)
            return Response({'success': 'Subtask added successfully'}, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, id):
        todo_item = TodoItem.objects.get(id=id)
        serializer = TodoInputSerializer(todo_item, data=request.data)
        if serializer.is_valid():
            TodoItemService.update(id, **serializer.validated_data)
            return Response({'success': 'Todo updated successfully'}, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        todo_item = TodoItem.objects.get(id=id)
        todo_item.delete()
        return Response({'success': 'Todo deleted successfully'},status=204)
    
class TodoItemActionView(APIView):
    def post(self, request, id):
        todo = TodoItem.objects.get(id=id)
        action = request.data['action']
        content = request.data['content']
        if action == 'rename':
            TodoItemService.rename(todo, content)
        elif action == 'check':
            TodoItemService.check(todo)
        elif action == 'uncheck':
            TodoItemService.uncheck(todo)
        elif action == 'move':
            old_group = content['old_group']
            new_group = content['new_group']
            TodoItemService.move(old_group, new_group, todo)
        else:
            return Response({'error': 'Invalid action'}, status=400)
        return Response({'success': action +' performed successfully'}, status=200)
    


class TodoGroupListView(APIView):
    def get(self, request):
        todo_groups = TodoGroup.objects.all()
        serializer = GroupOutputSerializer(todo_groups, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GroupInputSerializer(data=request.data)
        if serializer.is_valid():
            TodoGroupService.create(**serializer.validated_data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TodoGroupFilterView(APIView):
    def get(self, request):
        todos = TodoGroup.objects.all()
        groups = request.data.get('groups', None)
        todos = todos.filter(Q(groups=groups))
        serializer = GroupOutputSerializer(todos, many=True)
        return Response(serializer.data)

class TodoGroupDetailView(APIView):
    def get(self, request, id):
        todo_group = TodoGroup.objects.get(id=id)
        serializer = GroupOutputSerializer(todo_group)
        return Response(serializer.data)
    
    def put(self, request, id):
        todo_group = TodoGroup.objects.get(id=id)
        serializer = GroupInputSerializer(todo_group, data=request.data)
        if serializer.is_valid():
            TodoGroupService.update(id, **serializer.validated_data)
            return Response({'success': 'Group updated successfully'}, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        todo_group = TodoGroup.objects.get(id=id)
        todo_group.delete()
        return Response({'success': 'Group deleted successfully'}, status=204)

class TodoGroupActionView(APIView):
    def post(self, request, id):
        group = TodoGroup.objects.get(id=id)
        action = request.data['action']
        content = request.data['content']
        if action == 'rename':
            TodoGroupService.rename_group(group, content)
        elif action == 'add_todo':
            TodoGroupService.add_todo(group, content)
        elif action == 'remove_todo':
            TodoGroupService.remove_todo(group, content)
        elif action == 'add_group':
            TodoGroupService.add_group(group, content)
        elif action == 'remove_group':
            TodoGroupService.remove_group(group, content)
        elif action == 'move_group':
            old_group = content['old_group']
            new_group = content['new_group']
            TodoGroupService.move_group(old_group, new_group, group)
        else:
            return Response({'error': 'Invalid action'}, status=400)
        return Response({'success': action +' performed successfully'}, status=200)
    

class TodoSubtaskActionView(APIView):
    def post(self, request, id):
        subtask = Subtask.objects.get(id=id)
        action = request.data['action']
        content = request.data['content']
        if action == 'rename':
            SubtaskService.rename(subtask, content)
        elif action == 'check':
            SubtaskService.check(subtask)
        elif action == 'uncheck':
            SubtaskService.uncheck(subtask)
        else:
            return Response({'error': 'Invalid action'}, status=400)
        return Response({'success': action +' performed successfully'}, status=200)
    
    def delete(self, request, id):
        subtask = Subtask.objects.get(id=id)
        subtask.delete()
        return Response({'success': 'Subtask deleted successfully'},status=204)
    
class TodoSubtaskActionView(APIView):
    def post(self, request, id):
        subtask = Subtask.objects.get(id=id)
        action = request.data['action']
        content = request.data['content']
        if action == 'rename':
            SubtaskService.rename(subtask, content)
        elif action == 'check':
            SubtaskService.check(subtask)
        elif action == 'uncheck':
            SubtaskService.uncheck(subtask)
        elif action == 'remove':
            SubtaskService.remove(subtask)
        elif action == 'move':
            SubtaskService.move(subtask, int(content))
        else:
            return Response({'error': 'Invalid action'}, status=400)
        return Response({'success': action +' performed successfully'}, status=200)
    
    def delete(self, request, id):
        subtask = Subtask.objects.get(id=id)
        subtask.delete()
        return Response({'success': 'Subtask deleted successfully'},status=204)