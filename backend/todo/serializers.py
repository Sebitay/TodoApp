from rest_framework import serializers
from .models import TodoItem, TodoGroup, Subtask


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)

def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


class StringListField(serializers.ListField):
    child = serializers.CharField()

class GroupInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    groups = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all(), many=True)
    todos = serializers.PrimaryKeyRelatedField(queryset=TodoItem.objects.all(), many=True)

class TodoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    date = serializers.DateField()
    checked = serializers.BooleanField()
    group = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all())
    subtasks = StringListField()

class SubtaskInputSerializer(serializers.Serializer):
    todo = serializers.PrimaryKeyRelatedField(queryset=TodoItem.objects.all())
    index = serializers.IntegerField()
    content = serializers.CharField(max_length=256)


class SubtaskOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    index = serializers.IntegerField()
    checked = serializers.BooleanField()
    content = serializers.CharField(max_length=256)

class GroupOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    groups = serializers.PrimaryKeyRelatedField(queryset=TodoGroup.objects.all(), many=True)
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

