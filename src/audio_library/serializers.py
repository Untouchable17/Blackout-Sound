from rest_framework import serializers

from src.audio_library import models
from src.base.services import delete_old_file
from src.oauth.serializers import ProfileSerializer


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):

    class Meta:
        model = models.Genre
        fields = ("id", "title")


class LicenseSerializer(BaseSerializer):

    class Meta:
        model = models.License
        fields = ("id", "description")


class AlbumSerializer(BaseSerializer):

    class Meta:
        model = models.Album
        fields = ("id", "title", "description", "picture", "private")

    def update(self, instance, validated_data):
        delete_old_file(instance.picture.path)
        return super().update(instance, validated_data)


class CreateAuthorTrackSerializer(BaseSerializer):

    plays_count = serializers.IntegerField(read_only=True)
    download_count = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Track
        exclude = ("likes_count", "likes")

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)     # удаление файла
        delete_old_file(instance.picture.path)  # удаление обложки
        return super().update(instance, validated_data)


class AuthorTrackSerializer(CreateAuthorTrackSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    user = ProfileSerializer()


class CreatePlayListSerializer(BaseSerializer):

    class Meta:
        model = models.PlayList
        fields = ("id", "title", "picture", "tracks")

    def update(self, instance, validated_data):
        delete_old_file(instance.picture.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):

    tracks = AuthorTrackSerializer(many=True, read_only=True)


class CommentAuthorSerializer(serializers.ModelSerializer):
    """ Сериализатор комментариев """

    class Meta:
        model = models.Comment
        fields = ("id", "text", "track")


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализация комментариев """

    user = ProfileSerializer()

    class Meta:
        model = models.Comment
        fields = ("id", "text", "user", "track", "created_at")