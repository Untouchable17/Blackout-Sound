from rest_framework import serializers

from src.oauth import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AuthUser
        fields = ("avatar", "display_name", "country", "city", "biography")


class SocialLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SocialLink
        fields = ("link", )


class ProfileSerializer(serializers.ModelSerializer):

    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.AuthUser
        fields = (
            "id",
            "avatar",
            "display_name",
            "country",
            "city",
            "biography",
            "social_links"
        )