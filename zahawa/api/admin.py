from django.contrib import admin

from . import models

admin.site.register(models.Vendors)

admin.site.register(models.Events)
admin.site.register(models.Image)
admin.site.register(models.Services)
admin.site.register(models.VendorsReview)
admin.site.register(models.Proposals)
admin.site.register(models.Order)
