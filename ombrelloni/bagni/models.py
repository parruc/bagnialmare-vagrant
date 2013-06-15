from django.contrib.gis.db import models

# Create your models here.

class Bagno(models.Model):
    name = models.CharField(max_length=50)
    point = models.PointField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name
