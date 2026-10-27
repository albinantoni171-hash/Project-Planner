from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    DEVELOPER = 'Developer', 'Developer'
    PROJECT_COORDINATOR = 'Project Coordinator','Project Coordinator'

class Profile(AbstractUser):
    role = models.CharField(max_length=20, choices=RoleChoices.choices)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.username

    