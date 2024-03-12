from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from account.models import UserProfile

from . import choices
from .paystack import Paystack

User = get_user_model()


class PaymentTransaction(models.Model):
    """General Payment transaction model"""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Auth User"),
    )
    payment_method = models.CharField(
        _("Payment method"),
        max_length=20,
        choices=choices.PAYMENT_GATEWAY,
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        _("Amount"), default=0, max_digits=19, decimal_places=2
    )
    transaction_reason = models.CharField(
        _("Transaction Reason"), max_length=25, blank=True, null=True
    )
    amount = models.DecimalField(
        _("Actual Amount"), max_digits=19, decimal_places=2, blank=True, null=True
    )
    transaction_fee = models.DecimalField(
        _("Transaction Fee"),
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True,
    )
    flag = models.CharField(
        _("Flag"),
        choices=choices.TRANSACTION_FLAGS,
        max_length=25,
        null=True,
        blank=True,
    )
    status = models.CharField(
        _("Status"),
        choices=choices.TRANSACTION_STATUS,
        default="pending",
        max_length=15,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}"

    def mark_as_success(self):
        if self.status == "pending":
            self.status = "success"
            self.save()

    def mark_as_failed(self):
        if self.status == "pending":
            self.status = "failed"
            self.save()


class PaystackTransaction(models.Model):
    """
    Paystack Payment Gateway transaction model
    """

    transaction = models.OneToOneField(
        PaymentTransaction, related_name="paystack", on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        _("Amount in Naira"),
        max_digits=19,
        decimal_places=2,
    )
    reference = models.CharField(
        _("Payment Reference Number"), max_length=50, unique=True
    )
    fee = models.DecimalField(
        _("Paystack Fee"),
        max_digits=14,
        decimal_places=2,
        default=0.00,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.transaction.__str__()

    def set_reference(self):
        """
        This will set a progressive reference number that is always unique
        """
        now = timezone.now()
        str_date = str(now.date()).replace("-", "")
        prefix = "PT"  # Don't ever change this Prefix.
        self.reference = f"{prefix}{self.transaction.id}{str_date}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Set reference if it's a new object.
            self.set_reference()
        super().save(*args, **kwargs)
