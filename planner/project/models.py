from django.db import models

# Create your models here.

import uuid
from django_ckeditor_5.fields import CKEditor5Field


class BaseClass (models.Model):
    uuid = models.UUIDField(unique=True,default=uuid.uuid4)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta : 
         abstract = True


class Project(BaseClass):
    name = models.CharField(max_length=100)
    description = CKEditor5Field()
    document = models.FileField(upload_to='project-documents')

    class Meta :
        verbose_name = 'projects'
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.name

class AssignedProjects(BaseClass):
    project = models.ForeignKey('project',on_delete=models.PROTECT,related_name='project')
    coordinator = models.ForeignKey('authentication.profile',on_delete=models.PROTECT,related_name='coordinator')
    developers = models.ManyToManyField('authentication.profile')
    project_duration = models.IntegerField()
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True,blank=True)


    class Meta :
            verbose_name = 'Assigned projects'
            verbose_name_plural = 'Assigned projects'
    
    def __str__(self):
            return f'{self.project.name}-{self.project_start_date}'

class PriorityChoices(models.TextChoices):
     LOW = 'Low', 'Low'
     MEDIUM = 'Medium', 'Medium'
     HIGH = 'High', 'High'
    
class Task(BaseClass):
    assigned_project = models.ForeignKey('AssignedProjects',on_delete=models.PROTECT,related_name='task_project')
    assigned_to = models.ForeignKey('authentication.profile',on_delete=models.PROTECT,related_name='task_assigned_to')
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=100, choices=PriorityChoices.choices)
    duration = models.TimeField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f'{self.assigned_project.project.name}-{self.assigned_to.first_name}-{self.title}'