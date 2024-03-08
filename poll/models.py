from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import UserProfile


class Poll(models.Model):

    question = models.CharField(_("Question"), max_length=225)
    is_paid = models.BooleanField(_("Is Paid"), default=False)
    is_closed = models.BooleanField(_("Is Closed"), default=False)
    amount = models.DecimalField(_("Amount"), decimal_places=2, max_digits=9, default=0)
    poll_type = models.CharField(_("Poll Type"), max_length=50, blank=True, null=True)
    poll_access = models.CharField(
        _("Poll Access"), max_length=50, blank=True, null=True
    )
    creator = models.ForeignKey(
        to=UserProfile,
        verbose_name=_("Creator"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    voters = models.ManyToManyField(
        to=UserProfile, verbose_name=_("Voters"), related_name="poll_voters", blank=True
    )
    close_time = models.DateTimeField(_("Close Time"), blank=True, null=True)
    media_file = models.FileField(
        _("Media"), upload_to="poll-media-files", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.question


class PollOption(models.Model):

    content = models.CharField(_("Content"), max_length=225)
    poll = models.ForeignKey(
        to=Poll,
        on_delete=models.CASCADE,
        verbose_name=_("Poll"),
        related_name="options",
    )
    voters = models.ManyToManyField(
        to=UserProfile, verbose_name=_("Voters"), related_name="voters", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.content
