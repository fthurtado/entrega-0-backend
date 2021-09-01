import jwt
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

from backend.users.models import ClientUser

class IsClientUser(BasePermission):
    message = "User not found"

    def has_permission(self, request, _):
        if not request.headers.get("Authorization"):
            return False

        if request.headers["Authorization"].split()[0] != "Bearer":
            return False

        try:
            token = request.headers["Authorization"].split()[1]
            jwt.decode(
                token,
                settings.JWT_KEY,
                algorithms=["HS256"],
                verify_exp=False,
            )
            decoded = jwt.decode(
                token, settings.JWT_KEY, algorithms=["HS256"], verify_exp=False
            )
            client_user = ClientUser.objects.get(pk=decoded["id"])

            if client_user is None:
                raise AuthenticationFailed(
                    detail=self.message
                )
            return True

        except (IndexError, KeyError):
            raise AuthenticationFailed()
