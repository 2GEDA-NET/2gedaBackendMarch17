from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import User


class Face_Detection(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_("corresponding user"), on_delete=models.CASCADE
    )
    image = models.ImageField(_("image data"), upload_to="images")
    time_stamp = models.DateTimeField(default=timezone.now)
