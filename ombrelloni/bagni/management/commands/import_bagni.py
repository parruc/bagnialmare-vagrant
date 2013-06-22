from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from bagni.models import Bagno, Service
from optparse import make_option
import simplejson

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        )

    def handle(self, *args, **options):
        bagni = []
        cities = ["cervia", "cesenatico", "ferrara", "ravenna"]
        fields = ["name", "number", "address", "city", "tel", "fax", "site", "mail"]
        for city in cities:
            try:
                with open('scripts/scraping/output_' + city + '.json', 'r') as output_file:
                    bagni += simplejson.load(output_file)
            except IOError:
                raise CommandError("cannot open 'scripts/scraping/output_" + city + ".json' Have you generated it?")

        if options['limit'] and options['limit'] > len(bagni):
            bagni = bagni[:options['limit']]
        for bagno in bagni:
            b = Bagno(name=bagno['name'])
            for field in fields:
                if field in bagno:
                    setattr(b, field, bagno[field])
            if "coords" in bagno and len(bagno['coords']) == 2:
                b.point = Point(bagno['coords'])
            #XX PORCATA TEMPORANEA finche non riesco a togliere NOT NULL da point
            else:
                b.point = Point(0,0)
            b.save()
            if "services" in bagno:
                for service in bagno['services']:
                    s = Service.objects.filter(name=service)
                    if s:
                        b.services.add(s[0])

            b.save()
