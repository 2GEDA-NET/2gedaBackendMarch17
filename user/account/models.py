from django.db import models
from django.utils.translation import gettext as _

# from location_field.models.plain import PlainLocationField

from ..auth.models import User
from django.conf import settings

COUNTS = {1000: "k", 1000000: "m", 1000000000: "b"}

RELIGION_CHOICES = [
    ("Christianity", "Christianity"),
    ("Muslim", "Muslim"),
    ("Indigenous", "Indigenous"),
    ("Others", "Others"),
]

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Rather not say", "Rather not say"),
)


DAYS_OF_THE_WEEK_CHOICES = (
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)


class ProfileMedia(models.Model):
    media = models.FileField(upload_to="profile_files/", blank=True, null=True)
    media_type = models.CharField(_("Type of media"), max_length=20, blank=True)


class CoverImageMedia(models.Model):
    media = models.FileField(upload_to="cover_files/", blank=True, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(_("User Bio"), blank=True, null=True)
    occupation = models.CharField(_("Occupation"), max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(_("Date of birth"), blank=True, null=True)
    gender = models.CharField(
        _("Gender"), max_length=15, choices=GENDER_CHOICES, blank=True, null=True
    )
    religion = models.CharField(
        _("Religion"), max_length=20, choices=RELIGION_CHOICES, blank=True, null=True
    )
    media = models.ForeignKey(
        ProfileMedia,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_media",
    )
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="cover-images", blank=True, null=True
    )
    profile_picture = models.ImageField(
        _("Profile Image"), upload_to="profile-images", blank=True, null=True
    )
    is_flagged = models.BooleanField(_("Is flagged"), default=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def stickers_count(self):
        return self.stickers.count()

    @property
    def profile_image(self):
        try:
            url = self.profile_picture.url
        except ValueError:
            url = ""
        return url

    @property
    def sticking_count(self):
        return 0  # TODO coming to this later


class Sticker(models.Model):
    sticker = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        verbose_name=_("Sticker"),
        related_name="stickers",
        help_text=_("stickers are like a followers"),
    )
    sticked = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        verbose_name=_("Sticked"),
        related_name="sticking",
        help_text=_("sticking are like those the user is following"),
    )
    sticked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["sticker", "sticked"]


class UserAddress(models.Model):
    """A model representing a user address."""

    profile = models.ForeignKey(
        UserProfile, verbose_name=_("Profile"), on_delete=models.CASCADE
    )
    country = models.CharField(
        _("Country"), max_length=20, default="Nigeria", blank=True, null=True
    )
    state = models.CharField(_("State"), max_length=50, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    street_address = models.CharField(
        _("Street Address"), max_length=100, blank=True, null=True
    )
    zip_code = models.CharField(_("Zip Code"), max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.street_address

    class Meta:
        verbose_name = _("User Address")
        verbose_name_plural = _("User Addresses")


# class BusinessAvailability(models.Model):
#     always_available = models.BooleanField(default=False)
#     # Define availability for each day of the week
#     # sunday
#     sunday = models.BooleanField(default=False)
#     sunday_open = models.TimeField(null=True, blank=True)
#     sunday_close = models.TimeField(null=True, blank=True)
#     # monday
#     monday = models.BooleanField(default=False)
#     monday_open = models.TimeField(null=True, blank=True)
#     monday_close = models.TimeField(null=True, blank=True)
#     # tuesday
#     tuesday = models.BooleanField(default=False)
#     tuesday_open = models.TimeField(null=True, blank=True)
#     tuesday_close = models.TimeField(null=True, blank=True)
#     # wednesday
#     wednesday = models.BooleanField(default=False)
#     wednesday_open = models.TimeField(null=True, blank=True)
#     wednesday_close = models.TimeField(null=True, blank=True)
#     # thursday
#     thursday = models.BooleanField(default=False)
#     thursday_open = models.TimeField(null=True, blank=True)
#     thursday_close = models.TimeField(null=True, blank=True)
#     # friday
#     friday = models.BooleanField(default=False)
#     friday_open = models.TimeField(null=True, blank=True)
#     friday_close = models.TimeField(null=True, blank=True)
#     # saturday
#     saturday = models.BooleanField(default=False)
#     saturday_open = models.TimeField(null=True, blank=True)
#     saturday_close = models.TimeField(null=True, blank=True)

#     def __str__(self):
#         return f"Availability for {self.user.username}"


class ReportedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    is_banned = models.BooleanField(default=False, verbose_name="Banned")
    is_disabled = models.BooleanField(default=False, verbose_name="Disabled")


class Verification(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    legal_name = models.CharField(max_length=250)
    work = models.CharField(max_length=250)
    link1 = models.URLField(max_length=250)
    link2 = models.URLField(max_length=250)
    link3 = models.URLField(max_length=250)
    media = models.ImageField(upload_to="verificationImage/", blank=True, null=True)


DEVICE_CATEGORY = (("IMEI", "IMEI"), ("SERIAL NUMBER", "SERIAL NUMBER"))


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    category = models.CharField(max_length=250, choices=DEVICE_CATEGORY)
    input = models.CharField(max_length=250)


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications_received"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications_sent"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient.username} from {self.sender.username}: {self.message}"


class BlockedUser(models.Model):
    blocker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blocked_users"
    )
    blocked_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blockers"
    )
    reason = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked_user}"

    class Meta:
        unique_together = ("blocker", "blocked_user")
