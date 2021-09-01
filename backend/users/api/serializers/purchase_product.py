from rest_framework import serializers
from backend.users.models import Purchase, PurchaseProductRequest, Product


class PurchaseSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField("get_product")
    class Meta:
        model = Purchase
        fields = ["id", "verification_code", "created_at", "client_user", "product"]

    def get_product(self, purchase: Purchase):
        product = purchase.purchase_product_details.all()[0].product

        data = {
            "client_user": product.client_user.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": purchase.purchase_product_details.all()[0].product_quantity,
        }

        return data

class PurchaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseProductRequest
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

