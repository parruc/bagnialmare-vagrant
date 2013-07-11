from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
import autoslug

# Create your models here.


class Bagno(models.Model):
    """ The model for Bagno object
    """
    class Meta:
        verbose_name = _('Bagno')
        verbose_name_plural = _('Bagni')

    name = models.CharField(max_length=60)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True)
    number = models.CharField(max_length=15, blank=True)
    services = models.ManyToManyField("Service", blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    mail = models.EmailField(max_length=50, blank=True)
    tel = models.CharField(max_length=75, blank=True)
    fax = models.CharField(max_length=50, blank=True)
    site = models.URLField(max_length=75, blank=True)
    point = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("bagno", [self.slug, ])


class Service(models.Model):
    """ The model for Service object
    """
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    BEACH = "BE"
    SPORT = "SP"
    RENT = "RE"
    OTHER = "OT"
    SERVICE_CATEGORIES = (
        (BEACH, _('Beach')),
        (SPORT, _('Sport')),
        (RENT, _('Rent')),
        (OTHER, _('Other')),
    )

    name = models.CharField(max_length=50)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True)
    category = models.CharField(max_length=50,
                                blank=True,
                                choices=SERVICE_CATEGORIES,
                                default=OTHER)
    free = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        return ("service", [self.slug, ])

    def __unicode__(self):
        return self.name

