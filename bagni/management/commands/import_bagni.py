from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from bagni.models import Bagno, Service, Municipality, District, Language
from optparse import make_option
import simplejson
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        )

    def handle(self, *args, **options):
        logger.info("Importing Bagni, Languages, Municipalities and Districts")
        Bagno.objects.all().delete()
        bagni = []
        cities = ["cervia", "cesenatico", "ferrara", "ravenna", "rimini", "riccione", "bellaria-igea-marina"]
        fields = ["name", "number", "address", "tel", "cell", "winter_tel", "fax", "site", "mail",]
        for city in cities:
            try:
                with open('scripts/scraping/output_' + city + '.json', 'r') as output_file:
                    bagni += simplejson.load(output_file)
            except IOError:
                raise CommandError("cannot open 'scripts/scraping/output_" + city + ".json' Have you generated it?")

        if 'limit' in options and options['limit'] > len(bagni):
            bagni = bagni[:options['limit']]
        languages = {}
        for language in ['Italian', 'English', 'Franch', 'German', 'Russian']:
            l = Language(name=language)
            l.save()
            languages[language] = l
        for bagno in bagni:
            b = Bagno(name=bagno['name'])
            for field in fields:
                if field in bagno:
                    setattr(b, field, bagno[field])
            if "coords" in bagno:
                b.point = Point([float(coord) for coord in reversed(bagno['coords'])])
            b.save()
            b.languages.add(languages['Italian'])
            b.languages.add(languages['English'])
            if "municipality" in bagno:
                d = District.objects.filter(name=bagno['municipality'])
                m = None
                if not d:
                    d = District(name=bagno['municipality'])
                    d.save()
                else:
                    d = d[0]
                if "neighbourhood" in bagno:
                    m = Municipality.objects.filter(name=bagno['neighbourhood'])
                    if not m :
                        m = Municipality(name=bagno['neighbourhood'])
                        m.district = d
                        m.save()
                    else:
                        m = m[0]
                if m and d:
                    b.municipality = m
            if "services" in bagno:
                for service in bagno['services']:
                    s = Service.objects.filter(name=service)
                    if s:
                        b.services.add(s[0])

            b.save()
