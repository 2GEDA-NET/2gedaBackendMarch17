from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from storages.backends.s3boto3 import S3Boto3Storage
from pydub import AudioSegment
from .models import Song
from datetime import timedelta

@receiver(post_save, sender=Song)
def set_song_duration(sender, instance, **kwargs):
    try:
        # Open the file using Django storage's open method
        with instance.audio_file.open('rb') as audio_file:
            audio = AudioSegment.from_file(audio_file)
        duration_seconds = audio.duration_seconds
        instance.duration = timedelta(seconds=duration_seconds)
    except Exception as e:
        # Log the exception or handle it accordingly
        raise ValidationError(f"Error calculating audio duration: {e}")