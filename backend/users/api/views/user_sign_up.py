from argon2 import PasswordHasher
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.users.api.serializers.user import ClientUserSerializerSignUp, ClientUserSerializer
from backend.users.models import ClientUser

class ClientUserSignUp(ModelViewSet):
    permission_classes = [AllowAny]
    renderer_classes = [CamelCaseJSONRenderer]
    http_method_names = ["post"]
    queryset = ClientUser.objects.all()
    serializer_class=ClientUserSerializerSignUp

    def email_exists(self, request):
        # Check if email already exists
        return ClientUser.objects.filter(email=request.data["email"]).exists()

    def nick_name_exists(self, request):
       # Check if nick_name already exists
        return ClientUser.objects.filter(nick_name=request.data["nick_name"]).exists()

    def create(self, request):
        password = request.data["password"]
        instance = PasswordHasher()
        hashed_password =  instance.hash(password)
        try:
            if self.email_exists(request):
                msg = {"message": "Email already exists"}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            if self.nick_name_exists(request):
                msg = {"message": "Nickname already exists"}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            client_user = {
              "nick_name": request.data["nick_name"],
              "email": request.data["email"].lower(),
              "password": hashed_password,
            }
            serializer_user = self.get_serializer(data=client_user)
            serializer_user.is_valid(raise_exception=True)
            user = serializer_user.save()

            data = ClientUserSerializer(user).data

            return Response(data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response(
                {"message": f"Missing key {e}"}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
