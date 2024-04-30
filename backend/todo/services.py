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

    @staticmethod
    def move_todo(old_group, new_group, todo_id):
        TodoGroupService.remove_todo(old_group, todo_id)
        TodoGroupService.add_todo(new_group, todo_id)

    @staticmethod
    def add_subtask(todo, content):
        subtask = Subtask.objects.create(todo=todo, content=content, index=len(todo.subtasks.all()))
        todo.subtasks.add(subtask)
    
    @classmethod
    def create(cls, **validated_data):
        subtasks = validated_data.pop('subtasks')
        group = validated_data.pop('group', None)
        todo = super().create(**validated_data)

        for i in range(len(subtasks)):
            subtask = Subtask.objects.create(todo=todo, content=subtasks[i], index=i)
            todo.subtasks.add(subtask)
            
        if group is not None:
            group = TodoGroup.objects.get(id=todo.group.id)
            TodoGroupService.add_todo(group, todo.id)

        return todo

    @classmethod
    def update(cls, id, **validated_data):
        subtasks = validated_data.pop('subtasks')
        todo = cls.model.objects.filter(id=id)
        todo.update(**validated_data)
        todo = cls.model.objects.get(id=id)

        for i in range(1,len(subtasks)+1):
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

    @classmethod
    def add_group(cls, group, group_to_add):
        verify = cls.verify_group(group, group_to_add)
        if verify['status']:
            group.childs.add(group_to_add)
            group_to_add.parent = group
            group_to_add.save()
            return verify
        else: return verify

    @staticmethod
    def remove_group(group, group_to_remove):
        group.childs.remove(group_to_remove)
        group_to_remove.parent = None
        group_to_remove.save()
    
    @classmethod
    def move_group(cls, old_group, new_group, group):
        verify = cls.verify_group(new_group, group)
        if verify['status']:
            TodoGroupService.remove_group(old_group, group)
            TodoGroupService.add_group(new_group, group)
            return verify
        else: return verify

    @classmethod
    def verify_group(cls, parent_group, child_group):
        if parent_group is None:
            return {'success': 'Group verified successfully', 'status': True}
        else:
            if parent_group == child_group:
                return {'error': 'Group cannot be parent of itself', 'status': False}
            elif parent_group == child_group.parent:
                return {'error': 'Group allready has this parent', 'status': False}
            elif parent_group.parent == child_group:
                return {'error': 'Child group found in parent family', 'status': False}
            else:
                return cls.verify_group(parent_group.parent, child_group)

    @classmethod
    def create(cls, **validated_data):
        todos = validated_data.pop('todos')
        childs = validated_data.pop('childs')
        parent = validated_data.pop('parent', None) 
        group = super().create(**validated_data, parent=parent)

        group.todos.set(todos)

        if parent is not None:
            cls.add_group(parent, group.id)

        for child in childs:
            cls.add_group(group, child.id)

        return group
    
    @classmethod
    def update(cls, id, **validated_data):
        todos = validated_data.pop('todos')
        childs = validated_data.pop('childs')
        group = cls.model.objects.get(id=id)
        cls.rename_group(group, validated_data.get('name'))
        cls.change_parent(group, validated_data.pop('parent', None))

        group.todos.clear()
        group.todos.set(todos)

        group.childs.clear()

        for child in childs:
            cls.add_group(group, child.id)

        return group

class SubtaskService(Service):
    model = Subtask

    @staticmethod
    def rename(subtask, new_content):
        subtask.content = new_content
        subtask.save()
    
    @staticmethod
    def check(subtask):
        subtask.checked = True
        subtask.save()
    
    @staticmethod
    def uncheck(subtask):
        subtask.checked = False
        subtask.save()
    
    @staticmethod
    def move(subtask_to_move, index):
        old_index = subtask_to_move.index

        if old_index == index:
            return
        todo = TodoItem.objects.get(id=subtask_to_move.todo.id)
        for subtask in todo.subtasks.all().order_by('index'):
            if old_index > index:
                if subtask.index >= index and subtask.index < old_index:
                    subtask.index += 1
                    subtask.save()
                else:
                    print(subtask.index, subtask.content)
            else:
                if subtask.index > old_index and subtask.index <= index:
                    subtask.index -= 1
                    subtask.save()
                else:
                    print(subtask.index, subtask.content)

        subtask_to_move.index = index
        subtask_to_move.save()

    @staticmethod
    def remove(subtask):
        index = subtask.index
        subtask.delete()
        todo = TodoItem.objects.get(id=subtask.todo.id)
        for subtask in todo.subtasks.all():
            if subtask.index > index:
                subtask.index -= 1
                subtask.save()
    
    @classmethod
    def create(cls, **validated_data):
        return super().create(**validated_data)