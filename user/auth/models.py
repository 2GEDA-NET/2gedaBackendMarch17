import random
import string

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext as _

from notifications import send_verification_code


# ------------------------------- AUTH ---------------------------------------- #
class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    """

    def _create_user(
        self, username, email, phone_number=None, password=None, **extra_fields
    ):
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
        user = self.model(
            username=username, email=email, phone_number=phone_number, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, username, email, phone_number=None, password=None, **extra_fields
    ):
        """
        Creates and saves a regular User with the
        given email, phone number, and password.
        """
        extra_fields.setdefault("is_verified", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_personal", True)
        return self._create_user(
            username, email, phone_number, password, **extra_fields
        )

    def create_business_user(
        self, username, email, phone_number=None, password=None, **extra_fields
    ):
        """
        Creates and saves a business User with the
        given email, phone number, and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_business", True)
        extra_fields.setdefault("is_personal", False)
        return self._create_user(
            username, email, phone_number, password, **extra_fields
        )

    def create_superuser(
        self, username, email, phone_number=None, password=None, **extra_fields
    ):
        """
        Creates and saves a superuser with the
        given email, phone number, and password.
        """
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(
            username, email, phone_number, password, **extra_fields
        )


class User(AbstractUser):
    # email = models.EmailField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, default=0)
    is_business = models.BooleanField(default=False, verbose_name="Business Account")
    is_personal = models.BooleanField(default=False, verbose_name="Personal Account")
    is_admin = models.BooleanField(default=False, verbose_name="Admin Account")
    phone_number = models.CharField(unique=True, max_length=20, default=0)
    # phone_number = models.BigIntegerField(unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name="Verified")
    last_seen = models.DateTimeField(null=True, blank=True)
    # otp = models.CharField(max_length=5, blank=True)
    # otp_verified = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=64)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    class Meta:
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return str(self.username) or ""

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
        ("password_verification", "Password Verification"),
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
        send_verification_code(self.user, self.verification_type)


# ------------------------------- AUTH ---------------------------------------- #