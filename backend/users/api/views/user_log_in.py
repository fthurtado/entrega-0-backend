from argon2 import exceptions, PasswordHasher
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.users.api.serializers.user import ClientUserSerializer
from backend.users.models import ClientUser


class ClientUserLogIn(ModelViewSet):
    permission_classes = [AllowAny]
    renderer_classes = [CamelCaseJSONRenderer]
    http_method_names = ["post"]

    def verify_password(self, data):
        if data.get("email"):
            user = ClientUser.objects.get(email=data["email"].lower())
        else:
            user = ClientUser.objects.get(nick_name=data["nick_name"])
        # Check if password is correct
        instance = PasswordHasher()
        instance.verify(user.password, data["password"])
        return user

    def create(self, request):
        try:
            data = request.data
            user = self.verify_password(data)
            data = ClientUserSerializer(user).data

            return Response(data, status=status.HTTP_200_OK)
        except ClientUser.DoesNotExist:
            msg = {"message": "User does not exists"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        except exceptions.VerifyMismatchError:
            msg = {"message": "Incorrect Password"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
