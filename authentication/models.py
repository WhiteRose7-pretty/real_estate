from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    link = models.CharField(max_length=100, null=True, default='')

    def __str__(self):
        return self.email
