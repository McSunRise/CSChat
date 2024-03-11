from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class User(AbstractUser):
    __uuid = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    def create_user(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email
# Create your models here.
