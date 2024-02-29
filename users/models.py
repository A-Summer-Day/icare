from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)
    username = models.CharField(
        unique=True, 
        max_length=100,
        error_messages={
            'unique': 'A user with that username already exists.'
        })
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return self.full_name()