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
        categories = {}
        try:
            with open('scripts/scraping/services.json', 'r') as services_file:
                services += simplejson.load(services_file)
        except IOError:
            raise CommandError("cannot open 'scripts/scraping/services.json' Have you generated it?")

        try:
            with open('scripts/scraping/services_categories.json', 'r') as categories_file:
                categories.update(simplejson.load(categories_file))
        except IOError:
            raise CommandError("cannot open 'scripts/scraping/services_categories.json'. Try to git pull")

        if 'limit' in options and options['limit'] > len(services):
            services = services[:options['limit']]
        for service in services:
            try:
                s = Service(name=service)
                if service in categories:
                    s.category = categories.get(service, '')
                s.save()
            except:
                import ipdb; ipdb.set_trace()
