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
        Bagno.objects.all().delete()
        bagni = []
        cities = ["cervia", "cesenatico", "ferrara", "ravenna", "rimini", "riccione"]
        fields = ["name", "number", "address", "city", "tel", "cell", "winter_tel", "fax", "site", "mail"]
        for city in cities:
            try:
                with open('scripts/scraping/output_' + city + '.json', 'r') as output_file:
                    bagni += simplejson.load(output_file)
            except IOError:
                raise CommandError("cannot open 'scripts/scraping/output_" + city + ".json' Have you generated it?")

        if options['limit'] and options['limit'] > len(bagni):
            bagni = bagni[:options['limit']]
        for bagno in bagni:
            try:
                b = Bagno(name=bagno['name'])
                for field in fields:
                    if field in bagno:
                        setattr(b, field, bagno[field])
                if "coords" in bagno:
                    b.point = Point([float(coord) for coord in reversed(bagno['coords'])])
                b.save()
                if "services" in bagno:
                    for service in bagno['services']:
                        s = Service.objects.filter(name=service)
                        if s:
                            b.services.add(s[0])

                b.save()
            except Exception as e:
                print e
                import ipdb; ipdb.set_trace()
