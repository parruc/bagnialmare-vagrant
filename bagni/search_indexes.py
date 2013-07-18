import os
import re

from django.db.models import signals
from django.conf import settings

from whoosh import fields, index, qparser
from whoosh.filedb.filestore import FileStorage

from bagni.models import Bagno

WHOOSH_SCHEMA = fields.Schema(id=fields.ID(stored=True, unique=True),
                              name=fields.TEXT(stored=True),
                              text=fields.TEXT,
                              city=fields.ID(stored=True, ),
                              services=fields.IDLIST(stored=True, expression=re.compile("#")),
                            )

def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
        storage = FileStorage(settings.WHOOSH_INDEX)
        return index.Index(storage, schema=WHOOSH_SCHEMA, create=True)

signals.post_syncdb.connect(create_index)

def update_index(sender, obj, created, **kwargs):
    storage = FileStorage(settings.WHOOSH_INDEX)
    ix = index.Index(storage, schema=WHOOSH_SCHEMA)
    writer = ix.writer()
    if created:
        writer.add_document(id=unicode(obj.slug), name=unicode(obj.name),
                            text=obj.index_text(), city=unicode(obj.city),
                            services=unicode(obj.index_services(sep="#")),
        )
    else:
        writer.update_document(id=unicode(obj.slug), name=unicode(obj.name),
                            text=obj.index_text(), city=unicode(obj.city),
                            services=unicode(obj.index_services(sep="#")),
        )
    writer.commit()

signals.post_save.connect(update_index, sender=Bagno)

def search(query, facets, filters):

    storage = FileStorage(settings.WHOOSH_INDEX)
    ix = index.Index(storage, schema=WHOOSH_SCHEMA)
    hits = []
    # Whoosh don't understands '+' or '-' but we can replace
    # them with 'AND' and 'NOT'.
    query = query.replace('+', ' AND ').replace(' -', ' NOT ')
    og = qparser.OrGroup.factory(0.9)
    parser = qparser.QueryParser("text", schema=ix.schema, group=og)
    parser.remove_plugin_class(qparser.WildcardPlugin)
    try:
        qry = parser.parse(query)
    except:
        # don't show the user weird errors only because we don't
        # understand the query.
        # parser.parse("") would return None
        qry = None
    if qry is not None:
        searcher = ix.searcher()
        hits = searcher.search(qry)
