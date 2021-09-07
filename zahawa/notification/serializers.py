from rest_framework import serializers

from . import models


class SendedNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SendedNotification
        fields = [
            "pk",
            "type",
            "content",
            "timestamp",
            "subtitle",
            "image",
            "active_request",
            "related_user",
        ]
