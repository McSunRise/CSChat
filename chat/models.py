from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def create_user(self, username, email, password):
        self.username = username
        self.set_password(password)
        self.email = email
