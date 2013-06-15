from django.contrib.gis import admin
import models

admin.site.register(models.Bagno, admin.GeoModelAdmin)
