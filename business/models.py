from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from account.models import UserProfile


class BusinessAccount(models.Model):

    class Category(models.TextChoices):
        personal = ("personal", "personal")
        company = ("company", "company")

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("Auth User"),
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(
        to=UserProfile,
        verbose_name=_("Profile"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    business_name = models.CharField(_("Business Name"), max_length=50)
    address = models.CharField(_("Address"), max_length=250, blank=True, null=True)
    biz_phone_numbers = ArrayField(
        models.CharField(max_length=20),
        verbose_name=_("Business phone numbers"),
        blank=True,
        null=True,
    )
    display_picture = models.ImageField(
        _("Business Display Picture"),
        upload_to="business-pictures/",
        blank=True,
        null=True,
    )
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="cover-images/", blank=True, null=True
    )
    category = models.CharField(
        _("Category"), max_length=20, choices=Category.choices, blank=True, null=True
    )
    bio = models.TextField(_("Bio"), blank=True, null=True)
    # business_email = models.EmailField(_("Business Email"), blank=True, null=True)
    website_link = models.CharField(_("Website"), max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(_("Verified"), default=False)
    founded_on = models.DateField(_("Founded On"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.business_name


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
    id_image = models.ImageField(
        _("Government issued ID"),
        upload_to="business-verify-images",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.business.business_name


# class PhoneNumber(models.Model):

#     business = models.ForeignKey(
#         to=BusinessAccount, verbose_name=_("Business"), on_delete=models.CASCADE
#     )
#     phone1 = models.CharField(_("Phone 1"), max_length=20, blank=True, null=True)
#     phone2 = models.CharField(_("Phone 2"), max_length=20, blank=True, null=True)
#     phone3 = models.CharField(_("Phone 3"), max_length=20, blank=True, null=True)
#     phone4 = models.CharField(_("Phone 4"), max_length=20, blank=True, null=True)

#     def __str__(self):
#         return self.business


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
