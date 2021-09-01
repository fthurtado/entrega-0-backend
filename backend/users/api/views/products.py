import jwt
from django.conf import settings
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from backend.users.helpers.is_client_user import IsClientUser
from backend.users.models import ClientUser, Product
from backend.users.api.serializers.purchase_product import ProductSerializer


class ClientUserProducts(ModelViewSet):
    permission_classes = [IsClientUser]
    renderer_classes = [CamelCaseJSONRenderer]
    http_method_names = ["get"]

    def list(self, request):
        token = request.headers["Authorization"].split()[1]
        decoded = jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"], verify_exp=False)
        client_user = ClientUser.objects.get(pk=decoded["id"])
        if client_user is None:
            return Response(
                {"message": "Authorization error"}, status=status.HTTP_403_FORBIDDEN
            )
        products = client_user.products.all()
        data = ProductSerializer(products, many=True).data
        return Response(data, status.HTTP_200_OK)


class Products(ModelViewSet):
    permission_classes = [IsClientUser]
    renderer_classes = [CamelCaseJSONRenderer]
    http_method_names = ["get"]

    def list(self, request):
        token = request.headers["Authorization"].split()[1]
        decoded = jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"], verify_exp=False)
        client_user = ClientUser.objects.get(pk=decoded["id"])
        if client_user is None:
            return Response(
                {"message": "Authorization error"}, status=status.HTTP_403_FORBIDDEN
            )
        products = Product.objects.filter(activated=True).exclude(client_user=client_user.id)
        data = ProductSerializer(products, many=True).data
        return Response(data, status.HTTP_200_OK)


class NewProduct(ModelViewSet):
    permission_classes = [IsClientUser]
    renderer_classes = [CamelCaseJSONRenderer]
    http_method_names = ["post"]

    def create(self, request):
        data = request.data
        token = request.headers["Authorization"].split()[1]
        decoded = jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"], verify_exp=False)
        client_user = ClientUser.objects.get(pk=decoded["id"])

        if client_user is None:
            return Response(
                {"message": "Authorization error"}, status=status.HTTP_403_FORBIDDEN
            )

        product = {
          "client_user": client_user.id,
          "name": data["product"]["name"],
          "description": data["product"]["description"],
          "price": data["product"]["price"],
          "quantity": data["product"]["quantity"],
          "first_quantity": data["product"]["quantity"],
        }

        product_serializer= ProductSerializer(data=product)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()

        return Response(
            {"message": "Product created successfully"}, status=status.HTTP_201_CREATED,
        )
