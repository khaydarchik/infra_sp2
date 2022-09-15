from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
        help_text='Биография пользователя.'
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=200,
        choices=ROLE,
        default='user',
        help_text='Выберите роль пользователя.'
    )
    email = models.EmailField(
        verbose_name='email adress',
        unique=True,
        help_text='Введите email пользователя.'
    )
    confirmation_code = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"

    def __str__(self):
        return self.username
