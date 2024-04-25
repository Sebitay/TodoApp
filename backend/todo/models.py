from django.db import models

class TodoGroup(models.Model):
    name = models.CharField(max_length=256)
    todos = models.ManyToManyField('TodoItem', blank=True)
    groups = models.ManyToManyField('self', blank=True, default=None, symmetrical=False)
    def __str__(self):
        return self.name
    

class TodoItem(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    checked = models.BooleanField(default=False)
    group = models.ForeignKey('TodoGroup', on_delete=models.CASCADE, blank=True, null=True)
    subtasks = models.ManyToManyField('Subtask', blank=True)
    repeat = models.CharField(max_length=256, default='', blank=True)
    

class Subtask(models.Model):
    todo = models.ForeignKey('TodoItem', on_delete=models.CASCADE)
    index = models.IntegerField()
    content = models.CharField(max_length=256)
    checked = models.BooleanField(default=False)
    def __str__(self):
        return self.content