from rest_framework import serializers
from .models import TodoItem, TodoGroup, Subtask
from django.contrib.auth.models import User


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)

def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)

class StringListField(serializers.ListField):
    child = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class GroupInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    childs = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all(), many=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all(), required=False)
    todos = serializers.PrimaryKeyRelatedField(queryset=TodoItem.objects.all(), many=True)

class TodoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    date = serializers.DateField()
    checked = serializers.BooleanField()
    group = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all(), required=False)
    subtasks = StringListField()

class SubtaskInputSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=256)


class SubtaskOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    index = serializers.IntegerField()
    checked = serializers.BooleanField()
    content = serializers.CharField(max_length=256)

class GroupOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    childs = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all(), many=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all())
    todos = serializers.PrimaryKeyRelatedField(queryset=TodoItem.objects.all(), many=True)

class TodoOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=256)
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    date = serializers.DateField()
    checked = serializers.BooleanField()
    group = inline_serializer(fields={
        'id': serializers.IntegerField(),
        'name': serializers.CharField(max_length=256)
    })
    subtasks = SubtaskOutputSerializer(many=True)

