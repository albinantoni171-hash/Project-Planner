from uuid import uuid4

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.models import Profile, RoleChoices


class TaskListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.unknown_uuid = uuid4()
        self.developer = Profile.objects.create_user(
            username='task-api-developer',
            password='test-password',
            role=RoleChoices.DEVELOPER,
        )

    def test_get_tasks_for_unknown_assigned_project_returns_404(self):
        response = self.client.get(f'/tasks/{self.unknown_uuid}/')

        self.assertEqual(response.status_code, 404)

    def test_create_task_for_unknown_assigned_project_returns_404(self):
        response = self.client.post(
            f'/tasks/{self.unknown_uuid}/',
            {
                'assigned_to': self.developer.pk,
                'title': 'Test task',
                'description': 'Test task description',
                'priority': 'Medium',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 404)
