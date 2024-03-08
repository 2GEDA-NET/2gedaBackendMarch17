from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import UserProfile

from . import choices


class Notification(models.Model):

    profile = models.ForeignKey(
        to=UserProfile, on_delete=models.CASCADE, verbose_name=_("User Profile")
    )
    action = models.CharField(
        _("Action"),
        max_length=50,
        choices=choices.NOTIFICATION_ACTIONS,
        blank=True,
        null=True,
    )
    content = models.TextField(_("Notification Content"), blank=True, null=True)
    is_seen = models.BooleanField(_("Seen"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # more fields here...

    def __str__(self) -> str:
        return self.content
