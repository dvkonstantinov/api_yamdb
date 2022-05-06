from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        verbose_name='Адрес эл.почты',
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=100,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Немного о себе',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
