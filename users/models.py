import random

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from catalog.models import NULLABLE





from config import settings


# Create your models here.

class User(AbstractUser):

    word_list = list("Password12345")
    ver_code = "".join(random.sample(word_list, len(word_list)))

    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='media/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    country = models.CharField(max_length=235, verbose_name='страна', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активен')
    verification_code = models.CharField(max_length=35, verbose_name='код верификации', default=ver_code)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
