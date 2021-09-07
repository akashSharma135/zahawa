from django.shortcuts import render

from fcm_django.models import FCMDevice

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser as User

# from api.models import Event, Post, Product

from . import models
from . import serializers

import _thread as thread


def send_notification(msg, users, type, obj, img=None, title=None):
    try:
        thread.start_new_thread(log_notifications, (users, msg, type, obj, img, title))
        devices = FCMDevice.objects.all().filter(user__in=users)
        devices.send_message(title=title, body=msg)
    except Exception:
        pass


def log_notifications(users, msg, type, obj, img, title):
    # print(users, msg, order_status, obj, img, title)
    for user in users:
        try:
            user = User.objects.get(pk=user["user"])
        except:
            pass
        # if type == 'order_is_accepted':
        #     print(obj)
        models.SendedNotification.objects.create(
            type=type,
            user=user,
            content=msg,
            active_request=obj,
            image=img,
            subtitle=title,
        )


class SendedNotificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = models.SendedNotification.objects.filter(
            user=request.user
        ).order_by("-pk")
        serializer = serializers.SendedNotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class SendedNotificationTypes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = models.Notification.objects.values_list(
            "title", flat=True
        ).order_by("id")
        return Response({"types": notifications})
