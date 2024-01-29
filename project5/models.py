from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_user')
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    archived = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='#3788D8')  
    editable = models.BooleanField(default=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

