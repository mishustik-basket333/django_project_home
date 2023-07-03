from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


# Create your models here.

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='media/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    country = models.CharField(max_length=235, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
