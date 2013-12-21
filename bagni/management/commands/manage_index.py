from django.core.management.base import BaseCommand
from bagni import search
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-o", "--operation",
                    action="store", type="string",
                    dest="operation"),
        make_option("-l", "--language",
                    action="store", type="string",
                    dest="language"),
        )

    def handle(self, *args, **options):
        if not options['operation']:
            print "-o or --operation parameter required"

        if not options['language']:
            print "applying to all active languages"
            kwargs = {}
        else:
            kwargs = {'langs': [options['language']]}
        if options['operation'] == 'create':
            search.create_index(**kwargs)
        elif options['operation'] == 'delete':
            search.delete_index(**kwargs)
        elif options['operation'] == 'recreate':
            search.recreate_index(**kwargs)
        ## Reindex is evil because it double all entries in the index. Use rebuild instead
        ##elif options['operation'] == 'reindex':
        ##    search.recreate_data(**kwargs)
        elif options['operation'] == 'rebuild':
            search.recreate_all(**kwargs)
        else:
            print """Choose an operation using the -o parameter:
	            'create' to rebuild index schema (empty)
                'delete' to remove index schema and data
                'recreate' to delete and rebuild the index schema (empty)
                'rebuild' to remove and recreate both index and data
                """
                #'reindex' to reindex data in existing schema
