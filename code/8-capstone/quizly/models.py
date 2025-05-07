from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username
    
    def display_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    