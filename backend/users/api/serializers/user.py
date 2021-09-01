import jwt
from django.conf import settings
from rest_framework import serializers
from backend.users.models import ClientUser


class ClientUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = ClientUser
        fields = ["token", "id", "nick_name", "email", "confirmed_email"]

    def get_token(self, user):
        data = {"id": user.id}
        token = jwt.encode(data, settings.JWT_KEY, algorithm="HS256").decode("utf-8")

        return token

class ClientUserSerializerSignUp(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = "__all__"
