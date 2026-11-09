from django.urls import path
from . import views

urlpatterns = [

        path('projects/',views.ProjectListCreateView.as_view()),
        path('projects/<str:uuid>/',views.ProjectRetriveUpdateDestroyView.as_view()),
        path('assignedprojects/',views.AssignedProjectsListCreateView.as_view()),
        path('assignedprojects/<str:uuid>/',views.AssignedProjectsRetriveUpdateDestroyView.as_view()),
        path('tasks/<str:uuid>/',views.TaskListCreateView.as_view()),
        path('tasks-retrieve-update-destroy/<str:uuid>/',views.TaskRetriveUpdateDestroyView.as_view()),
        path('generate-tasks/<str:uuid>/',views.GenerateTaskWithAI.as_view()),
]