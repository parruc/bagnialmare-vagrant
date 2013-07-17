from django.core.management.base import BaseCommand, CommandError
from bagni.models import Service
from optparse import make_option
import simplejson

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        )

    def handle(self, *args, **options):
        Service.objects.all().delete()
        services = []
        try:
            with open('scripts/scraping/services.json', 'r') as services_file:
                services += simplejson.load(services_file)
        except IOError:
            raise CommandError("cannot open 'scripts/scraping/services.json' Have you generated it?")

        if options['limit'] and options['limit'] > len(services):
            services = services[:options['limit']]
        for service in services:
            s = Service(name=service)
            s.save()
