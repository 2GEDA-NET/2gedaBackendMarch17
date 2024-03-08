
from django.dispatch import receiver
from django.utils import timezone
from .models import Status
from .tasks import delete_expired_status
from django.db.models.signals import post_save




@receiver(post_save, sender=Status)
def schedule_status_deletion(sender, instance:Status, **kwargs):

    # Schedule the task to delete the status after 86400 seconds (24hrs)

    delete_expired_status.apply_async(args=[instance.id], countdown=86400)


