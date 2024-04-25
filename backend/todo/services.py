from .models import TodoItem, TodoGroup, Subtask


class Service():
    model = None

    @classmethod
    def create(cls, **kwargs):
        object = cls.model(**kwargs)

        object.full_clean()
        object.save()
        
        return object
    
    @classmethod
    def delete(cls, id):
        cls.model.objects.get(id=id).delete()


class TodoItemService(Service):
    model = TodoItem

    @staticmethod
    def rename(todo, new_title):
        todo.title = new_title
        todo.save()
    
    @staticmethod
    def check(todo):
        todo.checked = True
        todo.save()
    
    @staticmethod
    def uncheck(todo):
        todo.checked = False
        todo.save()

    @classmethod
    def create(cls, **validated_data):
        subtasks = validated_data.pop('subtasks')
        todo = super().create(**validated_data)

        for i in range(len(subtasks)):
            subtask = Subtask.objects.create(todo=todo, content=subtasks[i], index=i)
            todo.subtasks.add(subtask)

        group = TodoGroup.objects.get(id=todo.group.id)
        TodoGroupService.add_todo(group, todo.id)

        return todo

    @classmethod
    def update(cls, id, **validated_data):
        subtasks = validated_data.pop('subtasks')
        todo = cls.model.objects.filter(id=id)
        todo.update(**validated_data)
        todo = cls.model.objects.get(id=id)

        for i in range(len(subtasks)):
            if len(todo.subtasks) > i:
                if todo.subtasks[i].content != subtasks[i]:
                    todo.subtasks[i].content = subtasks[i]
                    todo.subtasks[i].index = i
                    todo.subtasks[i].save()
            else:
                subtask = Subtask.objects.create(todo=todo, content=subtasks[i], index=i)
                todo.subtasks.add(subtask)

        return todo


class TodoGroupService(Service):
    model = TodoGroup

    @staticmethod
    def rename_group(group, new_name):
        group.name = new_name
        group.save()

    @staticmethod
    def add_todo(group, todo_id):
        todo = TodoItem.objects.get(id=todo_id)
        group.todos.add(todo)
    
    @staticmethod
    def remove_todo(group, todo_id):
        group.todos.remove(todo_id)

    @staticmethod
    def add_group(group, new_group_id):
        new_group = TodoGroup.objects.get(id=new_group_id)
        group.groups.add(new_group)

    @staticmethod
    def remove_group(group, group_id):
        group.groups.remove(group_id)

    @classmethod
    def create(cls, **validated_data):
        todos = validated_data.pop('todos')
        groups = validated_data.pop('groups')
        group = super().create(**validated_data)

        group.groups.set(groups)
        group.todos.set(todos)

        return group
    
    @classmethod
    def update(cls, id, **validated_data):
        todos = validated_data.pop('todos')
        groups = validated_data.pop('groups')
        group = cls.model.objects.get(id=id)
        cls.rename_group(group, validated_data.get('name'))
 
        group.groups.clear()
        group.todos.clear()

        group.groups.set(groups)
        group.todos.set(todos)

        return group

class SubtaskService(Service):
    model = Subtask