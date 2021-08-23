from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'м'),
        (FEMALE, 'ж'),
    )
    user = models.OneToOneField(
        ShopUser,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )
    tagline = models.CharField(
        verbose_name='теги',
        max_length=128,
        blank=True
    )
    about_me = models.TextField(
        verbose_name='О себе',
        max_length=512,
        blank=True
    )
    gender = models.CharField(
        verbose_name='Пол',
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True
    )
    vk_profile_address = models.CharField(
        verbose_name='Профиль вконтакте',
        max_length=128,
        blank=True,
    )
    vk_language = models.CharField(
        verbose_name='Язык',
        max_length=32,
        blank=True,
    )

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
