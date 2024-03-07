from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import UserAddress, UserProfile
from authentication.models import User


@receiver(post_save, sender=User)
def create_instances(sender, instance, created, **kwargs):
    """
    Create a user profile when a new user is created.
    """
    if created:
        profile = UserProfile.objects.create(user=instance)
        UserAddress.objects.create(profile=profile)
