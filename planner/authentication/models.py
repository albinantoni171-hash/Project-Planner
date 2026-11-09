from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class RoleChoices(models.TextChoices):
    DEVELOPER = 'Developer','Developer'
    ADMIN = 'Admin','Admin'
    PROJECT_COORDINATOR = 'Project coordinator','Project coordinator'

class TechChoices(models.TextChoices):
    FRONTEND = 'Frontend Developer','Frontend Developer'
    BACKEND = 'Backend Developer','Backend Developer'   
    FULLSTACK = 'Fullstack Developer','Fullstack Developer'
    UIUX = 'UI/UX Designer','UI/UX Designer'
    TESTER = 'Software Tester','Software Tester'
    



class Profile (AbstractUser):
    role = models.CharField(max_length=100,choices=RoleChoices.choices)
    tech = models.CharField(max_length=100,choices=TechChoices.choices,blank=True,null=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return f'{self.username}-{self.role} - {self.tech}'