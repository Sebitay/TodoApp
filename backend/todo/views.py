import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User

from .models import TodoItem, TodoGroup, Subtask
from .services import TodoItemService, TodoGroupService, SubtaskService
from .serializers import TodoInputSerializer, TodoOutputSerializer, GroupInputSerializer, GroupOutputSerializer, SubtaskInputSerializer, UserSerializer


class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'error': 'Invalid password'}, status=400)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data}, status=200)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            user.set_password(serializer.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=201)
        return Response(serializer.errors, status=400)

class TestUserView(APIView): 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class TodoItemListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        todo_items = TodoItem.objects.filter(Q(user=request.user)).all()
        serializer = TodoOutputSerializer(todo_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoInputSerializer(data=request.data)
        if serializer.is_valid():
            TodoItemService.create(**serializer.validated_data, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TodoItemFilterView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        delta = request.data.get('date', None)
        group = request.data.get('group', None)
        checked = True if request.data.get('checked', None) == '1' else False

        todos = TodoItem.objects.filter(Q(user=request.user)).all()

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, id):
        todo_item = TodoItem.objects.get(id=id)

        if todo_item.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        serializer = TodoOutputSerializer(todo_item)
        return Response(serializer.data)
    
    def post(self, request, id):
        todo_item = TodoItem.objects.get(id=id)

        if todo_item.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        serializer = SubtaskInputSerializer(data=request.data)
        if serializer.is_valid():
            content = request.data['content']
            TodoItemService.add_subtask(todo_item, content)
            return Response({'success': 'Subtask added successfully'}, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, id):
        todo_item = TodoItem.objects.get(id=id)

        if todo_item.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        serializer = TodoInputSerializer(todo_item, data=request.data)
        if serializer.is_valid():
            TodoItemService.update(id, **serializer.validated_data)
            return Response({'success': 'Todo updated successfully'}, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        todo_item = TodoItem.objects.get(id=id)

        if todo_item.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        todo_item.delete()
        return Response({'success': 'Todo deleted successfully'},status=204)
    
class TodoItemActionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request, id):
        todo = TodoItem.objects.get(id=id)

        if todo.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        todo_groups = TodoGroup.objects.filter(Q(user=request.user)).all()
        serializer = GroupOutputSerializer(todo_groups, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GroupInputSerializer(data=request.data)
        if serializer.is_valid():
            TodoGroupService.create(**serializer.validated_data, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TodoGroupFilterView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        todos = TodoGroup.objects.filter(Q(user=request.user)).all()
        groups = request.data.get('groups', None)
        todos = todos.filter(Q(groups=groups))
        serializer = GroupOutputSerializer(todos, many=True)
        return Response(serializer.data)

class TodoGroupDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, id):
        todo_group = TodoGroup.objects.get(id=id)

        if todo_group.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        serializer = GroupOutputSerializer(todo_group)
        return Response(serializer.data)
    
    def put(self, request, id):
        todo_group = TodoGroup.objects.get(id=id)

        if todo_group.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        serializer = GroupInputSerializer(todo_group, data=request.data)
        if serializer.is_valid():
            TodoGroupService.update(id, **serializer.validated_data)
            return Response({'success': 'Group updated successfully'}, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        todo_group = TodoGroup.objects.get(id=id)

        if todo_group.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        todo_group.delete()
        return Response({'success': 'Group deleted successfully'}, status=204)

class TodoGroupActionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request, id):
        group = TodoGroup.objects.get(id=id)

        if group.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request, id):
        subtask = Subtask.objects.get(id=id)
        todo = subtask.todo

        if todo.user != request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        
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