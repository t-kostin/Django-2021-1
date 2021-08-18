from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст')
    activation_key = models.CharField(
        max_length=128,
        blank=True,
    )
    activation_key_expires = models.DateTimeField(
        default=now() + timedelta(hours=48),
    )

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def soft_delete(self):
        self.is_active = False
        self.save()
