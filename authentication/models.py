import random
import string

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from notifications import send_verification_code


# ------------------------------- AUTH ---------------------------------------- #
class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    """

    def _create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the
        given email and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email).lower().strip()
        username = username.lower()
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a regular User with the
        given email, and password.
        """
        extra_fields.setdefault("is_verified", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_personal", True)
        return self._create_user(email, username, password, **extra_fields)

    def create_business_user(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a business User with the
        given email, and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_business", True)
        extra_fields.setdefault("is_personal", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the
        given email, and password.
        """
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_business = models.BooleanField(_("Business Account"), default=False)
    is_personal = models.BooleanField(_("Personal Account"), default=False)
    is_admin = models.BooleanField(_("Admin Account"), default=False)
    is_verified = models.BooleanField(_("Verified"), default=False)
    secret_key = models.CharField(max_length=64)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email or self.username or "-"

    def generate_otp(self):
        otp = "".join(random.choices(string.digits, k=5))
        return otp

    def check_otp(self, otp):
        if hasattr(self, "one_time_password"):
            user_otp = self.one_time_password.filter(user=self, otp=otp)
            if user_otp.exists():
                return True
            return False
        return False


class OneTimePassword(models.Model):
    VERIFICATION_TYPE_OPTIONS = [
        ("account_verification", "Email Verification"),
        ("password_reset", "Password Reset"),
    ]
    user = models.ForeignKey(
        User,
        verbose_name=_("Auth User"),
        on_delete=models.CASCADE,
        related_name="one_time_password",
    )
    otp = models.CharField(_("OTP"), max_length=5)
    verification_type = models.CharField(
        _("Verification Type"),
        max_length=25,
        choices=VERIFICATION_TYPE_OPTIONS,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

    def send_code(self):
        # print("SEND CODE-----------")
        send_verification_code(self.user, self.verification_type)


# ------------------------------- AUTH ---------------------------------------- #
