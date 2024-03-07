from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from user.account.models import UserProfile

User = get_user_model()


class BusinessCategory(models.Model):

    name = models.CharField(_("Category Name"), max_length=250)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Mate:
        verbose_name = _("Business Category")
        verbose_name_plural = _("Business Categories")

    def __str__(self):
        return self.name


class BusinessAccount(models.Model):

    user = models.ForeignKey(
        to=User, verbose_name=_("Auth User"), on_delete=models.CASCADE
    )
    business_name = models.CharField(_("Business Name"), max_length=50)
    address = models.CharField(_("Address"), max_length=250, blank=True, null=True)

    business_image = models.ImageField(
        _("Business Image"), upload_to="business-images/", blank=True, null=True
    )
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="cover-images/", blank=True, null=True
    )
    category = models.ForeignKey(
        to=BusinessCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category",
        verbose_name=_("Business Category"),
    )
    about = models.TextField(_("About"), blank=True, null=True)
    business_email = models.EmailField(_("Business Email"), blank=True, null=True)
    website_link = models.CharField(_("Website"), max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(_("Verified"), default=False)
    founded_on = models.DateField(_("Founded On"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.business_name


class BusinessOwnerProfile(models.Model):

    profile = models.OneToOneField(
        to=UserProfile,
        blank=True,
        null=True,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,
        related_name="business_owner",
    )
    id_document_type = models.CharField(
        _("Identification Document Type"), max_length=50, blank=True, null=True
    )
    id_document_file = models.FileField(
        _("Identification Document Type"),
        upload_to="business-owner-docs",
        blank=True,
        null=True,
    )
    is_verified = models.BooleanField(_("Verified"), default=False)
    verified_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self


class BusinessVerification(models.Model):

    business = models.ForeignKey(
        to=BusinessAccount, verbose_name=_("Business"), on_delete=models.CASCADE
    )
    legal_name = models.CharField(_("Legal Name"), max_length=50, blank=True, null=True)
    work = models.CharField(
        _("Work or Profession"), max_length=50, blank=True, null=True
    )
    link1 = models.URLField(_("Link1"), blank=True, null=True)
    link2 = models.URLField(_("Link2"), blank=True, null=True)
    link3 = models.URLField(_("Link3"), blank=True, null=True)
    is_completed = models.BooleanField(_("Completed"), default=False)
    id_image = models.ImageField(_("Government issued ID"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.business.business_name


class BusinessDocument(models.Model):

    business = models.ForeignKey(
        to=BusinessAccount, verbose_name=_("Business"), on_delete=models.CASCADE
    )
    tax_id = models.CharField(_("Tax ID"), max_length=100, blank=True, null=True)
    document_type = models.CharField(
        _("Document Type"), max_length=100, blank=True, null=True
    )
    document_file = models.FileField(
        _("Document File"), upload_to="business-files/", blank=True, null=True
    )
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.business.name}"


class PhoneNumber(models.Model):

    business = models.ForeignKey(
        to=BusinessAccount, verbose_name=_("Business"), on_delete=models.CASCADE
    )
    phone1 = models.CharField(_("Phone 1"), max_length=20, blank=True, null=True)
    phone2 = models.CharField(_("Phone 2"), max_length=20, blank=True, null=True)
    phone3 = models.CharField(_("Phone 3"), max_length=20, blank=True, null=True)
    phone4 = models.CharField(_("Phone 4"), max_length=20, blank=True, null=True)

    def __str__(self):
        return self.business


class BusinessTimeAvailability(models.Model):
    open_from = models.TimeField(_("Open"))
    close_at = models.TimeField(_("Close"))

    def __str__(self) -> str:
        return f"{self.open_from} -- {self.close_at}"


class BusinessDayAvailability(models.Model):
    business = models.ForeignKey(
        to=BusinessAccount, verbose_name=_("Business"), on_delete=models.CASCADE
    )
    monday = models.ForeignKey(
        to=BusinessTimeAvailability,
        verbose_name=_("Monday"),
        on_delete=models.CASCADE,
        related_name="monday",
    )
    tuesday = models.ForeignKey(
        to=BusinessTimeAvailability,
        verbose_name=_("Tuesday"),
        on_delete=models.CASCADE,
        related_name="tuesday",
    )
    wednesday = models.ForeignKey(
        to=BusinessTimeAvailability,
        verbose_name=_("Wednesday"),
        on_delete=models.CASCADE,
        related_name="wednesday",
    )
    thursday = models.ForeignKey(
        to=BusinessTimeAvailability,
        verbose_name=_("Thursday"),
        on_delete=models.CASCADE,
        related_name="thursday",
    )
    friday = models.ForeignKey(
        to=BusinessTimeAvailability,
        verbose_name=_("Friday"),
        on_delete=models.CASCADE,
        related_name="friday",
    )
    saturday = models.ForeignKey(
        to=BusinessTimeAvailability,
        verbose_name=_("Saturday"),
        on_delete=models.CASCADE,
        related_name="saturday",
    )
    sunday = models.ForeignKey(
        to=BusinessTimeAvailability,
        verbose_name=_("Sunday"),
        on_delete=models.CASCADE,
        related_name="sunday",
    )
