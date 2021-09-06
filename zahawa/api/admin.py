from django.contrib import admin

from . import models

admin.site.register(models.Vendors)

admin.site.register(models.Events)
admin.site.register(models.ImageList)
admin.site.register(models.Services)
admin.site.register(models.VendorsReview)
admin.site.register(models.Proposals)
admin.site.register(models.Order)
admin.site.register(models.Packages)
admin.site.register(models.Room)
admin.site.register(models.Categories)
admin.site.register(models.Product)
admin.site.register(models.CustomUser)
admin.site.register(models.CreateCart)
admin.site.register(models.Cart)
admin.site.register(models.Member)
admin.site.register(models.Team)

