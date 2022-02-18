from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import (
    get_path_upload_picture_playlist,
    get_path_upload_picture_album,
    get_path_upload_track,
    validate_size_image, get_path_upload_picture_track,
)
from src.oauth.models import AuthUser


class License(models.Model):
    """ Модель лицензий трека пользователя """

    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="licenses")
    description = models.TextField(max_length=1700, verbose_name="Описание лицензии")


class Genre(models.Model):
    """ Модель жанров треков """

    title = models.CharField(max_length=30, unique=True, verbose_name="Жанр трека")

    def __str__(self):
        return self.title


class Album(models.Model):
    """ Модель альбома для треков """

    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=75, verbose_name="Заголовок альбома")
    description = models.TextField(max_length=700, verbose_name="Описание альбома")
    private = models.BooleanField(default=False, verbose_name="Приватность")
    picture = models.ImageField(
        upload_to=get_path_upload_picture_album,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image],
    )


class Track(models.Model):
    """ Модель треков """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="tracks")
    title = models.CharField(max_length=175, verbose_name="Заголовок песни")
    license = models.ForeignKey(License, on_delete=models.PROTECT, related_name="license_tracks", verbose_name="Лицензия песни")
    genre = models.ManyToManyField(Genre, related_name="track_genres", verbose_name="Жанр(ы) песни")
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    link_of_author = models.CharField(max_length=720, blank=True, null=True, verbose_name="Ссылка стороннего ресурса")
    file = models.FileField(
        upload_to=get_path_upload_track,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])],
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки файла")
    plays_count = models.PositiveIntegerField(default=0, verbose_name="Количество прослушиваний песни")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Количество загрузок песни")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Количество лайков")
    likes = models.ManyToManyField(AuthUser, related_name='likes_of_tracks')
    private = models.BooleanField(default=False, verbose_name="Приватность")
    picture = models.ImageField(
        upload_to=get_path_upload_picture_track,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image],
    )

    def __str__(self):
        return f"{self.user} -> {self.title}"


class Comment(models.Model):
    """ Модель коммента трека """

    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="comments")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="track_comments")
    text = models.TextField(max_length=1200, verbose_name="Содержимое комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания комментария")


class PlayList(models.Model):
    """ Модель плейлистов пользователя """

    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="play_lists")
    title = models.CharField(max_length=75, verbose_name="Заголовок плейлиста")
    tracks = models.ManyToManyField(Track, related_name="track_playlist", verbose_name="Треки в плейлисте")
    picture = models.ImageField(
        upload_to=get_path_upload_picture_playlist,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image],
    )



