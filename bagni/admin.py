from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from modeltranslation.admin import TranslationAdmin
import models


class BagnoAdmin(TranslationAdmin, GeoModelAdmin):
    pass

class DistrictAdmin(TranslationAdmin, GeoModelAdmin):
    pass

class MunicipalityAdmin(TranslationAdmin, GeoModelAdmin):
    pass

class ServiceAdmin(TranslationAdmin, GeoModelAdmin):
    pass

class ServiceCategoryAdmin(TranslationAdmin, GeoModelAdmin):
    pass

class LanguageAdmin(TranslationAdmin, GeoModelAdmin):
    pass

class ImageAdmin(TranslationAdmin, GeoModelAdmin):
    pass


admin.site.register(models.Bagno, BagnoAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.ServiceCategory, ServiceCategoryAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Municipality, MunicipalityAdmin)
admin.site.register(models.Language, LanguageAdmin)