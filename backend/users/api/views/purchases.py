import jwt
from django.conf import settings
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from backend.users.helpers.is_client_user import IsClientUser
from backend.users.models import ClientUser, Product
from backend.users.api.serializers.purchase_product import PurchaseSerializer, PurchaseProductSerializer

def verification_code_generator(client_user: ClientUser):
    first = "Entrega-0"

    middle = f"{'{:0>4}'.format(client_user.id)}"
    last = f"{'{:0>4}'.format(client_user.purchases.count() + 1)}"
    code = f"{first}-{middle}-{last}"
    return code


class Purchases(ModelViewSet):
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
        purchases = client_user.purchases.all()
        data = PurchaseSerializer(purchases, many=True).data
        return Response(data, status.HTTP_200_OK)


class NewPurchase(ModelViewSet):
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

        purchase = {
          "client_user": client_user.id,
          "verification_code": verification_code_generator(client_user),
        }

        purchase_serializer = PurchaseSerializer(data=purchase)
        purchase_serializer.is_valid(raise_exception=True)
        purchase = purchase_serializer.save()

        product = Product.objects.get(pk=data["product"]["id"])
        difference = product.quantity - data["product"]["quantity"]
        new_quantity = product.quantity - data["product"]["quantity"] if difference > 0 else 0
        if new_quantity == 0:
            product.quantity = new_quantity
            product.activated = False
            product.save(update_fields=["quantity", "activated"])
        else:
            product.quantity = new_quantity
            product.save(update_fields=["quantity"])

        purchase_product = {
          "purchase": purchase.id,
          "product": data["product"]["id"],
          "product_quantity": data["product"]["quantity"] if difference > 0 else difference + data["product"]["quantity"],
        }
        purchase_product_serializer = PurchaseProductSerializer(data=purchase_product)
        purchase_product_serializer.is_valid(raise_exception=True)
        purchase_product = purchase_product_serializer.save()

        return Response(
            {"message": "Purchase created successfully"}, status=status.HTTP_201_CREATED,
        )
