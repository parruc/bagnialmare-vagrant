from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from modeltranslation.admin import TranslationAdmin
import models


class BagnoAdmin(TranslationAdmin, GeoModelAdmin):
    pass


class ServiceAdmin(TranslationAdmin, GeoModelAdmin):
    pass


class ImageAdmin(TranslationAdmin, GeoModelAdmin):
    pass


admin.site.register(models.Bagno, BagnoAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Image, ImageAdmin)
