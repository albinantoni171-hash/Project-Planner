from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from .models import Project,AssignedProjects,Task
from .serializers import ProjectSerializer,AssignedProjectsSerializer,TaskSerializer
from rest_framework.response import Response
from planner.utils import generate_tasks
from django.db import transaction
from authentication.permissions import IsAdmin,IsProjectCoordinator,IsDevoloper
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ProjectListCreateView(ListCreateAPIView):
    queryset = Project.objects.filter(active_status =True)
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            permissions = [IsAdmin]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions] 

class ProjectRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    lookup_field='uuid'
    queryset = Project.objects.filter(active_status =True)
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
        
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            permissions = [IsAdmin]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions] 

    def perform_destroy(self,instance) :
        instance.active_status = False
        instance.save()

class AssignedProjectsListCreateView(ListCreateAPIView):
    queryset = AssignedProjects.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developers')
    serializer_class = AssignedProjectsSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            permissions = [IsAdmin,IsProjectCoordinator]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions] 

class AssignedProjectsRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    lookup_field='uuid'
    queryset = AssignedProjects.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developers')
    serializer_class = AssignedProjectsSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            permissions = [IsAdmin,IsProjectCoordinator]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def perform_destroy(self,instance) :
        instance.active_status = False
        instance.save()

class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            permissions = [IsProjectCoordinator]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions] 

    def get_assigned_project(self):
        return get_object_or_404(AssignedProjects, uuid=self.kwargs['uuid'])

    def get_queryset(self):
        assigned_project = self.get_assigned_project()
        tasks = Task.objects.filter(active_status=True,assigned_project=assigned_project)
        return tasks

    def perform_create(self,serializer):
        serializer.save(assigned_project=self.get_assigned_project())

class TaskRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    lookup_field='uuid'
    queryset = Task.objects.filter(active_status=True).select_related('assigned_project','assigned_to')
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
        
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            permissions = [IsProjectCoordinator]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions] 

    def perform_destroy(self,instance) :
        instance.active_status = False
        instance.save()

class GenerateTaskWithAI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsProjectCoordinator]

    def post(self,request,*args,**kwargs):
        uuid = kwargs.get('uuid')
        assigned_project = AssignedProjects.objects.get(uuid=uuid)
        response,developers = generate_tasks(assigned_project)
        tasks = [Task(
            assigned_project=assigned_project,
            assigned_to_id = task.developer_id,
            title = task.title,
            description = task.description,
            priority = task.priority
        ) 
        for task in response.tasks if task.developer_id in [dev.id for dev in developers]]

        with transaction.atomic():
            Task.objects.bulk_create(tasks)

        return Response(status=200)