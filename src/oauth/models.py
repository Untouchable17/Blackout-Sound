from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from src.base.services import get_path_upload_avatar, validate_size_image

#
# class Follower(models.Model):
#     """ Модель подписчика """
#     user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="owner")
#     subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="subscribers")
#
#     def __str__(self):
#         return f"{self.subscriber} подписан на {self.user}"


class SocialLink(models.Model):
    """ Ссылки на другие социальные сети (модель пользователя) """
    user = models.ForeignKey("AuthUser", on_delete=models.CASCADE, related_name="social_links")
    link = models.URLField(max_length=125, verbose_name="Ссылка")

    def __str__(self):
        return f"{self.user}"


class AuthUser(models.Model):
    """ Модель пользователя на платформе """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Профиль")
    email = models.EmailField(max_length=175, unique=True, verbose_name="Почта пользователя")
    display_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Никнейм пользователя")
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    social_link = models.ForeignKey(SocialLink, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Ссылка на соц.сеть",  related_name="social_links")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна проживания")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город проживания")
    biography = models.TextField(max_length=1700, blank=True, null=True, verbose_name="Биография пользователя")
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image],
        verbose_name="Аватар пользователя"
    )

    def __str__(self):
        return f"{self.email} -> {self.display_name}"

    def get_absolute_url(self):
        return reverse('profile:profile-view', kwargs={'id': self.pk})

    @property
    def is_authenticated(self):
        """ Возвращает True. Способ, чтобы узнать, был ли пользоваетль аутентифицирован """
        return True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AuthUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



