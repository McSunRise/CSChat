from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):

    username = models.CharField(
        unique=True,
        max_length=32,
        help_text="Required. 32 symbols maximum. Only letters, digits and ./@/_/+/- symbols",
        validators=[username_validator],
        error_messages={'unique': 'A user with that username already exists.'}
    )

    def create_user(self, username, email, password):
        self.username = username
        self.set_password(password)
        self.email = email
