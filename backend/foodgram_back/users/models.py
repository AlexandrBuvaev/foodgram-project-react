from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField("Имя пользователя", max_length=150)
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    email = models.EmailField("Адрес электронной почты", max_length=150,
                              unique=True)
    password = models.CharField("Пароль", max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
