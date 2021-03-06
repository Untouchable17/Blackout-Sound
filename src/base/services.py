import os

from django.core.validators import ValidationError


def get_path_upload_avatar(instance, file):
    """ Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg """

    return f"avatar/user_{instance.id}/{file}"


def validate_size_image(file_object):
    """ Проверка размера загружаемого файла """

    megabyte_limit = 2
    if file_object.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла не должен превышать {megabyte_limit}MB")


def get_path_upload_picture_album(instance, file):
    """ Построение пути к файлу, format: (media)/album/user_id/photo.jpg """

    return f"album/user_{instance.user.id}/{file}"



def get_path_upload_picture_playlist(instance, file):
    """ Построение пути к файлу, format: (media)/playlist/user_id/photo.jpg """

    return f"playlist/user_{instance.user.id}/{file}"




def delete_old_file(path_file):
    """ Удаление старого файла """

    if os.path.exists(path_file):
        os.remove(path_file)