from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
from rest_framework.authtoken.models import Token
from stereo.models import Library


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("User profile created for:", instance.username)
        profile = UserProfile.objects.create(user=instance)
        Library.objects.create(profile=profile)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("User profile saved for:", instance.username)
    instance.userprofile.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
