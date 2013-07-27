from django.core.management.base import BaseCommand, CommandError
from bagni import search
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-o", "--operation",
                    action="store", type="string",
                    dest="operation"),
        )

    def handle(self, *args, **options):
        if not options['operation']:
            print "-o or --operation parameter required"
        if options['operation'] == 'create':
            search.create_index()
        elif options['operation'] == 'delete':
            search.delete_index()
        elif options['operation'] == 'recreate':
            search.recreate_index()
        elif options['operation'] == 'reindex':
            search.recreate_data()
        elif options['operation'] == 'rebuild':
            search.recreate_all()
        else:
            print """Choose an operation using the -o parameter:
	            'create' to rebuild index schema (empty)
                'delete' to remove index schema and data
                'recreate' to delete and rebuild the index schema (empty)
                'reindex' to reindex data in existing schema
                'rebuild' to remove and recreate both index and data
                """
