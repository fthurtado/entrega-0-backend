from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """Default user for Backend."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


def greater_than_zero(value):
    if not value > 0:
        raise ValidationError(_("Fields must be greater than zero"))

class ClientUser(models.Model):
    nick_name = models.TextField(_("Nick Name"))
    email = models.EmailField(_("Email"), unique=True)
    password = models.TextField(_("Password"))
    confirmed_email = models.BooleanField(_("Confirmed email"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return f"{self.nick_name} - {self.email}"

class Product(models.Model):
    name = models.TextField(_("Name"))
    description = models.TextField(_("Description"), null=True, blank=True)
    price = models.FloatField(_("Price"), validators=[greater_than_zero])
    first_quantity = models.IntegerField(_("First Quantity"))
    quantity = models.IntegerField(_("Quantity"))
    activated = models.BooleanField(_("Activated"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    client_user = models.ForeignKey(
        ClientUser, on_delete=models.PROTECT, related_name="products"
    )

    def __str__(self):
        return self.name

class Purchase(models.Model):
    verification_code = models.TextField(_("Verification code"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    client_user = models.ForeignKey(
        ClientUser, on_delete=models.PROTECT, related_name="purchases"
    )

class PurchaseProductRequest(models.Model):
    product_quantity = models.IntegerField(_("Quantity"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    # Foreign Keys
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="purchase_product_details"
    )
    purchase = models.ForeignKey(
        Purchase, on_delete=models.PROTECT, related_name="purchase_product_details"
    )

    def __str__(self):
        return f"{self.purchase.verification_code} - {self.product.name}"

