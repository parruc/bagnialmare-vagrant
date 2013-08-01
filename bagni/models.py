from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField
import autoslug


class Bagno(models.Model):
    """ The model for Bagno object
    """
    class Meta:
        verbose_name = _('Bagno')
        verbose_name_plural = _('Bagni')

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True)
    number = models.CharField(max_length=15, blank=True)
    services = models.ManyToManyField("Service", blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    mail = models.EmailField(max_length=50, blank=True)
    tel = models.CharField(max_length=125, blank=True)
    cell = models.CharField(max_length=125, blank=True)
    winter_tel = models.CharField(max_length=75, blank=True)
    fax = models.CharField(max_length=125, blank=True)
    site = models.URLField(max_length=75, blank=True)
    point = models.PointField(geography=True, null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def services_ordered_by_category(self):
        """ Returns the list of services sorted by category.
            Useful for regoup templatetag in templates to avoid
            repeted items under different categories
        """
        return self.services.all().order_by("category")

    def index_text(self):
        """ Text indexed for fulltext search (the what field)
        """
        elems = (self.name, self.index_services(), self.city)
        return unicode("%s %s %s" % elems)

    def index_services(self, sep=" "):
        """ Returns a string representing all the bagno services separated by
            the sep varr.
            Needed to index the services as listid in whoosh and have facets
        """
        return unicode(sep.join([s.name for s in self.services.all()]))

    def index_features(self, sep="#"):
        """ Returns a dictionary representing the whoosh entry for
            the current object in the index
        """
        return dict(id=unicode(self.id),
                    text=self.index_text(),
                    city=unicode(self.city),
                    services=unicode(self.index_services(sep="#")),
                    )

    @models.permalink
    def get_absolute_url(self):
        return ("bagno", [self.slug, ])


class Service(models.Model):
    """ The model for Service object
    """
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    COMFORT = "CO"
    FOOD = "FO"
    SPORT = "SP"
    CHILDREN = "CH"
    TECH = "TE"
    ENTERTAINMENT = "EN"
    RENT = "RE"
    EVENTS = "EV"
    ACCESSIBILITY = "AC"
    EXTRA = "EX"
    BEAUTY = "BE"
    TRADE = "TR"
    PAYMENT = "PA"
    NOT_SET = "NS"
    SERVICE_CATEGORIES = (
        (COMFORT, _('comfort & relax')),
        (FOOD, _('food & beverage')),
        (SPORT, _('sport & wellness')),
        (CHILDREN, _('children')),
        (TECH, _('technology')),
        (ENTERTAINMENT, _('entertainment and games')),
        (RENT, _('rent')),
        (EVENTS, _('special events')),
        (ACCESSIBILITY, _('accessibility')),
        (EXTRA, _('extra services')),
        (BEAUTY, _('beauty & spa')),
        (TRADE, _('trade')),
        (PAYMENT, _('payment')),
        (NOT_SET, _('not set')),
    )

    name = models.CharField(max_length=50)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True)
    category = models.CharField(max_length=50,
                                blank=True,
                                choices=SERVICE_CATEGORIES,
                                default=NOT_SET)
    free = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        return ("service", [self.slug, ])

    def get_filtered_search_url(self):
        """ The search url to activate this (and only this) facet as filter
        """
        return reverse("search") + "?f=services:" + self.name

    def __unicode__(self):
        return self.name


class Image(models.Model):
    """ Model used for the bagno images
        TODO: inline in admin form of bagno?
    """
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    name = models.CharField(max_length=50)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True)
    image = ImageField(upload_to="images/bagni", verbose_name=_("Image"))
    bagno = models.ForeignKey(Bagno, verbose_name=_("Bagno"))
