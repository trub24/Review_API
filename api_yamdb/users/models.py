from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    USER_VALUE_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    ROLE_MAX_LENGTH,
    CODE_MAX_LENGTH
)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'админ'
        MODERATOR = 'moderator', 'модератор'
        USER = 'user', 'юзер'

    username = models.SlugField(
        'Имя пользователя',
        max_length=USER_VALUE_MAX_LENGTH,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=USER_VALUE_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=USER_VALUE_MAX_LENGTH,
        blank=True
    )
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Роль',
        max_length=ROLE_MAX_LENGTH,
        choices=Role.choices, default=Role.USER
    )
    confirmation_code = models.CharField(
        'Код поддтверждения',
        max_length=CODE_MAX_LENGTH
    )

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == self.Role.USER

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    class Meta:
        default_related_name = 'users'
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

    def __str__(self):
        return self.username
