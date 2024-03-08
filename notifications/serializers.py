from rest_framework import serializers

from . import models as m


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Notification
        exclude = ["profile"]
