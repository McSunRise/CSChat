from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):

    username = models.CharField(
        unique=True,
        max_length=32,
        help_text="Required. 32 symbols maximum. Only letters, digits and ./@/_/+/- symbols",
        validators=[username_validator],
        error_messages={'unique': 'A user with that username already exists.'}
    )
    profile_filename = models.CharField(blank=True)

    def create_user(self, username, email, password):
        self.username = username
        self.set_password(password)
        self.email = email

    def __str__(self):
        return self.username


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Участник"))

    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Отправитель"), on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name=_("Полученное сообщение+"), verbose_name=_("Получатель"), on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message
