from django.contrib import admin

# Register your models here.
from . import models


# class NotificationAdmin(admin.ModelAdmin):
#     pass
# readonly_fields = ['title']
#
# def has_add_permission(self, request):
#     return False
#
# def has_delete_permission(self, request, obj=None):
#     return False
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "subtitle")


class SendedNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "subtitle",
        "image",
        "user",
        "content",
        "timestamp",
        "active_request",
        "related_user",
    )


admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.SendedNotification, SendedNotificationAdmin)
