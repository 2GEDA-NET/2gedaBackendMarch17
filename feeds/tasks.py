from celery import shared_task
from django.utils import timezone

from feeds.models import Status


@shared_task
def delete_expired_status(status_id):
    try:
        status_instance = Status.objects.get(pk=status_id)

        expiration_time = status_instance.created_at + timezone.timedelta(seconds=30)

        if timezone.now() > expiration_time:
            status_instance.delete()
            status_instance.delete()

        return f"Status with ID {status_id} deleted successfully."
    except Status.DoesNotExist:
        return f"Status with ID {status_id} does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"
