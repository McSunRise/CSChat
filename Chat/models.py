from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class User(AbstractUser):
    __uuid = models.UUIDField()
    def create_user(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.uuid = uuid4()

# Create your models here.
